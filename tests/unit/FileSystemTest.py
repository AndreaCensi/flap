
import unittest

from flatexer.FileSystem import InMemoryFileSystem
from flatexer.path import Path, ROOT


class InMemoryFileSystemTest(unittest.TestCase):

    def setUp(self):
        self.fileSystem = InMemoryFileSystem() 
       
    def testThatCreatedFilesExist(self):
        path = Path.fromText("source.tex")
        self.fileSystem.createFile(path, "blah")
        
        file = self.fileSystem.open(path)
        
        self.assertTrue(file.exists())
        self.assertTrue(file.contains("blah"))


    def testThatMissingFileDoNotExist(self):
        path = Path.fromText("file\\that\\do\\not\\exist.txt")
        
        file = self.fileSystem.open(path)
        
        self.assertFalse(file.exists())


    def testContainingDirectoryIsAvailable(self):
        path = Path.fromText("my\\dir\\test.txt")
        self.fileSystem.createFile(path, "data")
        
        file = self.fileSystem.open(path) 
        
        self.assertEqual(file.container().path(), ROOT / "my" / "dir")
        
        
    def testFullNameIsAvailable(self):
        path = Path.fromText("/my/dir/test.txt")

        self.fileSystem.createFile(path, "data")
        
        file = self.fileSystem.open(path)
        
        self.assertEqual(file.fullname(), "test.txt")
        
        
    def testBasenameIsAvailable(self):
        path = Path.fromText("my/dir/test.txt")
        self.fileSystem.createFile(path, "whatever")

        file = self.fileSystem.open(path)
        
        self.assertEqual(file.basename(), "test")
        
        
    def testDirectoryContainsFiles(self):
        self.fileSystem.createFile(Path.fromText("dir/test.txt"), "x")
        self.fileSystem.createFile(Path.fromText("dir/test2.txt"), "y")
        
        file = self.fileSystem.open(Path.fromText("dir"))
        
        self.assertEqual(len(file.files()), 2)
        
        
    def testFilteringFilesInDirectory(self):
        self.fileSystem.createFile(Path.fromText("dir/test.txt"), "x")
        self.fileSystem.createFile(Path.fromText("dir/test2.txt"), "y")
        self.fileSystem.createFile(Path.fromText("dir/blah"), "z")
        
        file = self.fileSystem.open(Path.fromText("dir"))
        
        self.assertEqual(len(file.filesThatMatches("test")), 2)
        
        
    def testCopyingFile(self):
        source = Path.fromText("dir/test.txt")
        self.fileSystem.createFile(source, "whatever")
        
        file = self.fileSystem.open(source)
        
        destination = Path.fromText("dir2/clone")
        self.fileSystem.copy(file, destination)
        
        copy = self.fileSystem.open(destination / "test.txt")
        self.assertTrue(copy.exists())
        self.assertEqual(copy.content(), "whatever")
        
        
if __name__ == "__main__":
    unittest.main()