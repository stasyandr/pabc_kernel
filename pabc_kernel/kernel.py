from queue import Queue
from threading import Thread

from ipykernel.kernelbase import Kernel
import re
import subprocess
import tempfile
import os
import os.path as path

class RealTimeSubprocess(subprocess.Popen):
    """
    A subprocess that allows to read its stdout and stderr in real time
    """

    def __init__(self, cmd, write_to_stdout, write_to_stderr):
        """
        :param cmd: the command to execute
        :param write_to_stdout: a callable that will be called with chunks of data from stdout
        :param write_to_stderr: a callable that will be called with chunks of data from stderr
        """
        self._write_to_stdout = write_to_stdout
        self._write_to_stderr = write_to_stderr

        super().__init__(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0, text=True) # Сделал text=true. Если не писать, то ввод-вывод будет байтовый, но поток контроля ввода не работает. Если разобраться, можно будет назад перейти к байтовым потокам
        
        # self._write_to_stdout("Before _stdout_thread.start()\n")

        self._stdout_queue = Queue()
        self._stdout_thread = Thread(args=(self.stdout, self._stdout_queue))
        self._stdout_thread.daemon = True
        self._stdout_thread.start()
        # self._write_to_stdout("_stdout_thread.start()\n")

        self._stderr_queue = Queue()
        self._stderr_thread = Thread(args=(self.stderr, self._stderr_queue))
        self._stderr_thread.daemon = True
        self._stderr_thread.start()


class PabcKernel(Kernel):
    implementation = 'PascalABC.NET'
    implementation_version = '1.0'
    language = 'pascal'
    language_version = '3.8'
    language_info = {
        'name': 'pascal',
        'mimetype': 'text/pascal',
        'file_extension': '.pas',
    }
    banner = "PascalABC.NET kernel"
    
    files = []                
    
    def cleanup_files(self):
        """Remove all the temporary files created by the kernel"""
        for file in self.files:
            os.remove(file)
        os.remove(self.master_path)
        
    def new_temp_file(self, **kwargs):
        """Create a new temp file to be deleted when the kernel shuts down"""
        # We don't want the file to be deleted when closed, but only when the kernel stops
        kwargs['delete'] = False
        kwargs['mode'] = 'w'
        file = tempfile.NamedTemporaryFile(**kwargs)
        self.files.append(file.name)
        return file    
    
    def _write_to_stdout(self, contents):
        self.send_response(self.iopub_socket, 'stream', {'name': 'stdout', 'text': contents})

    def _write_to_stderr(self, contents):
        self.send_response(self.iopub_socket, 'stream', {'name': 'stderr', 'text': contents})

    def create_jupyter_subprocess(self, cmd):
        return RealTimeSubprocess(cmd,
                                  lambda contents: self._write_to_stdout(contents),
                                  lambda contents: self._write_to_stderr(contents))

    def compile_and_run_with_pabc(self, source_filename):
        args = [r'C:\Program Files (x86)\PABCCompilerRunner\PABCCompilerRunner.exe', source_filename]
        return self.create_jupyter_subprocess(args)    

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            stream_content = {'name': 'stdout', 'text': code + "\n"}        

        with self.new_temp_file(suffix='.pas') as source_file:
            source_file.write(code)
            source_file.flush()
            p = self.compile_and_run_with_pabc(source_file.name) 
            (stdout, stderr) = p.communicate()

            self.send_response(self.iopub_socket, 'stream', {'name': 'stdout', 'text': ""+stdout})

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    def do_shutdown(self, restart):
        """Cleanup the created source code files and executables when shutting down the kernel"""
        self.cleanup_files()
