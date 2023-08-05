import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jfx_bridge",
    version=subprocess.check_output("git describe", shell=True).decode("utf-8").strip(),
    author="justfoxing",
    author_email="justfoxingprojects@gmail.com",
    description="RPC bridge to/from Python2/Python3/Jython/etc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justfoxing/jfx_bridge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)