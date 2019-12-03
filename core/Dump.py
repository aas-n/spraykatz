# coding: utf-8

# Author:       Lyderic LEFEBVRE
# Twitter:      @lydericlefebvre
# Mail:         lylefebvre.infosec@gmail.com
# LinkedIn:     https://www.linkedin.com/in/lydericlefebvre
#
##############################################
#
# Thanks @HackAndDo for this amazing work.
# This code comes from https://beta.hackndo.com/remote-lsass-dump-passwords/
#
##############################################
#
class Dump(object):
    def __init__(self, smbConnection, filePath):
        self.__smbConnection = smbConnection
        self.__fpath = filePath
        self.__currentOffset = 0
        self.__tid = smbConnection.connectTree("C$")
        self.__fid = smbConnection.openFile(self.__tid, self.__fpath)
        self.__buffer_data = {}
        self.__buffer_data["offset"] = 0
        self.__buffer_data["size"] = 0
        self.__buffer_min_size = 4096
        self.__total_read = 0

    def close(self):
        self.__smbConnection.closeFile(self.__tid, self.__fid)


    def read(self, size):
        if size == 0:
            return b''
        
        if (self.__buffer_data["offset"] <= self.__currentOffset <= self.__buffer_data["offset"] + self.__buffer_data["size"] and self.__buffer_data["offset"] + self.__buffer_data["size"] > self.__currentOffset + size):
            value = self.__buffer_data["buffer"][self.__currentOffset - self.__buffer_data["offset"]:self.__currentOffset - self.__buffer_data["offset"] + size]
        else:
            self.__buffer_data["offset"] = self.__currentOffset
            
            if size < self.__buffer_min_size:
                value = self.__smbConnection.readFile(self.__tid, self.__fid, self.__currentOffset, self.__buffer_min_size)
                self.__buffer_data["size"] = self.__buffer_min_size
                self.__total_read += self.__buffer_min_size
            else:
                value = self.__smbConnection.readFile(self.__tid, self.__fid, self.__currentOffset, size)
                self.__buffer_data["size"] = size
                self.__total_read += size
            
            self.__buffer_data["buffer"] = value
        
        self.__currentOffset += size
        return value[:size]


    def seek(self, offset, whence=0):
        if whence == 0:
            self.__currentOffset = offset

    def tell(self):
        return self.__currentOffset
