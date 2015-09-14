#
# This file is part of Flap.
#
# Flap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flap.  If not, see <http://www.gnu.org/licenses/>.
#

from os import symlink
from unittest import TestCase
from flap.ui import main
from flap.path import TEMP


class LatexProject:
    """
    Data needed to defined the structure and content of a LaTeX project
    """

    IMAGE_CONTENT = "fake image content"
    RESOURCE_CONTENT = "fake resource content"

    def __init__(self):
        self.directory = TEMP / "flap-tests"
        self.root_latex_file = "main.tex"
        self.root_latex_code = "some latex code"
        self.parts = {}
        self.images_directory = "images"
        self.images = []
        self.resources = []

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, path):
        self._directory = path

    @property
    def root_latex_file(self):
        return self._root_latex_file

    @root_latex_file.setter
    def root_latex_file(self, path):
        self._root_latex_file = self._directory / path

    @property
    def images_directory(self):
        return self._images_directory

    @images_directory.setter
    def images_directory(self, path):
        self._images_directory = self._directory / path

    def create_on(self, file_system):
        file_system.deleteDirectory(self.directory)
        file_system.createFile(self.root_latex_file, self.root_latex_code)
        for (path, content) in self.parts.items():
            file_system.createFile(self.directory / path, content)
        for eachImage in self.images:
            file_system.createFile(self.images_directory / eachImage, LatexProject.IMAGE_CONTENT)
        for eachResource in self.resources:
            file_system.createFile(self.directory / eachResource, LatexProject.RESOURCE_CONTENT)


class FlapRunner:
    """
    Invoke FLaP, and provides access to the outputted files
    """

    def __init__(self, file_system, working_directory, output_directory):
        self._file_system = file_system
        self.working_directory = working_directory
        self.output_directory = output_directory
        self.merged_file = "merged.tex"

    @property
    def working_directory(self):
        return self._working_directory

    @working_directory.setter
    def working_directory(self, path):
        self._working_directory = path

    @property
    def output_directory(self):
        return self._output_directory

    @output_directory.setter
    def output_directory(self, directory):
        self._output_directory = directory

    @property
    def merged_file(self):
        return self.output_directory / self._merged_file

    @merged_file.setter
    def merged_file(self, path):
        self._merged_file = path

    def run_flap(self, project):
        root = self._file_system.forOS(project.root_latex_file)
        output = self._file_system.forOS(self.output_directory)
        main(["-v", root, output])

    def merged_content(self):
        return self.content_of(self._merged_file)

    def content_of(self, path):
        return self._file_system.open(self.output_directory / path).content()


class FlapVerifier(TestCase):
    """
    Verify the outputs produced by FLaP
    """

    def __init__(self, project, runner):
        super().__init__()
        self.project = project
        self._runner = runner

    def merged_content_is(self, expected):
        self.assertEqual(self._runner.merged_content(), expected)

    def images(self):
        for eachImage in self.project.images:
            self.assertEqual(self._runner.content_of(eachImage), LatexProject.IMAGE_CONTENT)

    def resources(self):
        for eachResource in self.project.resources:
            self.assertEqual(self._runner.content_of(eachResource), LatexProject.RESOURCE_CONTENT)

