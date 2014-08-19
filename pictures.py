# -*- coding: utf-8 -*-

import urllib2
import urlparse
import os.path
import logging

class PictureDownloader():
    def __init__(self):
        self.urls = []

    def read_file(self, infilepath):
        """ reads urls from input file,
            discards previously read urls,
            sets the download directory for pictures
            to directory of input file """
        self.urls = []
        if not os.path.isfile(infilepath):
            logging.warning('{0} is not a valid filepath. '
                            'No urls were loaded!'.format(infilepath))
        else:
            self.picture_dir = os.path.dirname(infilepath)
            with open(infilepath, 'r') as infile:
                for line in infile:
                    line = line.strip()
                    self.urls.append(line)

    def download(self):
        """ downloads pictures for loaded urls """
        for line in self.urls:
            path = urlparse.urlsplit(line).path
            filename = os.path.basename(path)
            try:
                urlfile = urllib2.urlopen(line)
            except urllib2.HTTPError as error:
                logging.warning('{0}: HTTP Error {1}: {2}'
                                .format(line, error.code, error.reason))
                continue
            content = urlfile.read()
            outfilepath = os.path.join(self.picture_dir, filename) 
            with open(outfilepath, 'w') as outfile:
                outfile.write(content)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        "-f", "--file", dest="filename",
        help="""input file, containing
 picture urls for pictures to be downloaded""",
        metavar="FILE")
    (options, args) = parser.parse_args()
    downloader = PictureDownloader()
    downloader.read_file(options.filename)
    downloader.download()
      	   
      
