# coding: utf-8

# Author:      @aas_s3curity
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
        self.__fileInfo = smbConnection.queryInfo(self.__tid, self.__fid)
        self.__endOfFile = self.__fileInfo.fields["EndOfFile"]
        self.__buffer_min_size = 1024 * 8
        self.__total_read = 0
        self.__buffer_data = {
                "offset": 0,
                "size": 0,
                "buffer": ""
        }

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
                value = self.__smbConnection.readFile(self.__tid, self.__fid, self.__currentOffset, size + self.__buffer_min_size)
                self.__buffer_data["size"] = size + self.__buffer_min_size
                self.__total_read += size
            
            self.__buffer_data["buffer"] = value
        
        self.__currentOffset += size
        return value[:size]


    def seek(self, offset, whence=0):
        if whence == 0:
            self.__currentOffset = offset
        elif whence == 1:
            self.__currentOffset += offset
        elif whence == 2:
            self.__currentOffset = self.__endOfFile - offset
        else:
            raise Exception('Seek function whence value must be between 0-2')

    def tell(self):
        return self.__currentOffset
