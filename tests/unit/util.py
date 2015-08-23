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

from unittest import TestCase, main
from unittest.mock import MagicMock, call, patch

from flap.util import Version, Release, SourceControl, Sources 
from distutils.dist import Distribution

class VersionTest(TestCase):
    
    def makeVersion(self, text):
        return Version.fromText(text)

    def verifyVersion(self, version, major, minor, micro):
        self.assertTrue(version.hasMajor(major))
        self.assertTrue(version.hasMinor(minor))
        self.assertTrue(version.hasMicro(micro))

    def testPrepareDevelopmentRelease(self):
        v1 = self.makeVersion("1.0.1")
        v2 = v1.nextMicroRelease()
        self.verifyVersion(v2, 1, 0, 2)

    def testPrepareMinorRelease(self):
        v1 = self.makeVersion("1.0")
        v2 = v1.nextMinorRelease()
        self.verifyVersion(v2, 1, 1, 0)
        
    def testPrepareMajorRelease(self):
        v1 = self.makeVersion("1.0")
        v2 = v1.nextMajorRelease()
        self.verifyVersion(v2, 2, 0, 0)
                
    def testEquality(self):
        v1 = self.makeVersion("1.3.dev1")
        self.assertTrue(v1 == v1)

    def testDifference(self):
        v1 = self.makeVersion("1.3.dev2")
        v2 = self.makeVersion("1.3.dev3")
        self.assertTrue(v1 != v2)

class SourcesTest(TestCase):
    
   
    def testReadVersion(self):
        with patch("flap.__version__", "1.3.4"):
            sources = Sources()
            version = sources.readVersion() 
            self.assertEqual(version, Version(1,3,4))            
        

class SourceControlTest(TestCase):
    
    def testCommit(self):
        mock = MagicMock()
        with patch("subprocess.call", mock):
            scm = SourceControl()
            scm.commit("my message")
        mock.assert_called_once_with(["git", "commit", "-m", "\"my message\""])


    def testTag(self):
        mock = MagicMock()
        with patch("subprocess.call", mock):
            scm = SourceControl()
            scm.tag(Version(2, 0, 1))
        mock.assert_has_calls([call(["git", "tag", "-a", "v2.0.1", "-m", "\"Version 2.0.1\""]),
                               call(["git", "push", "--tag"])])

class ReleaseTest(TestCase):
    
    
    def testDevelopmentRelease(self):
        sources = Sources()
        sources.readVersion = MagicMock()
        sources.readVersion.return_value = Version.fromText("1.3.3")
        sources.writeVersion = MagicMock()
                
        scm = SourceControl()
        scm.tag = MagicMock()
        scm.commit = MagicMock()
        
        release = Release(Distribution(), scm, sources)
        release.next = "micro"
        release.run()
        
        scm.tag.assert_called_once_with(Version(1, 3, 3))
        sources.readVersion.assert_called_once_with()
        sources.writeVersion.assert_called_once_with(Version(1, 3, 4))
        scm.commit.assert_has_calls([call("Releasing version 1.3.3"), 
                                     call("Preparing version 1.3.4")])
     
     
if __name__ == "__main__":
    main()