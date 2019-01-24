
import os, shutil, tempfile, git
from os.path import dirname

os.chdir(dirname(os.getcwd()))

from FELion_definitions import ErrorInfo, ShowInfo, recursive_overwrite

try:
    # Create temporary dir
    t = tempfile.mkdtemp()

    # Clone into temporary dir
    git.Repo.clone_from('https://github.com/aravindhnivas/FELion-Spectrum-Analyser', t, branch='master', depth=1)

    # Copy desired file from temporary dir
    recursive_overwrite(os.path.join(t, 'modules'), 'C:/FELion-GUI')

    # Remove temporary dir
    shutil.rmtree(t)
    ShowInfo("UPDATED", "Program is updated to the latest version.")

except Exception as e:
    ErrorInfo("ERROR: ", e)