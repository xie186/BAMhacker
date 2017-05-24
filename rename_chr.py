from __future__ import division
from argparse import ArgumentParser
#import pybedtools
import pysam

class Bam:
    
    def __init__(self):
         pass

    def renameChrom(self, options):
        """Rename chrom names"""
        bam = pysam.AlignmentFile(options.bam, 'rb')
        tem = pysam.AlignmentFile(options.template, 'rb')
        out = pysam.AlignmentFile(options.prefix + ".bam", "wb", template=tem)
        dict_chrom_ids = self.readChromInfo(options)
        print dict_chrom_ids
        for read in bam:
            #print str(read.reference_id) + " " + str(read.next_reference_id)
            ref_id1 = bam.get_reference_name(read.reference_id)  if read.reference_id != -1 else -1
            ref_id2 = bam.get_reference_name(read.next_reference_id) if read.next_reference_id != -1 else -1
            if (ref_id1 not in dict_chrom_ids and ref_id1 != -1) or (ref_id2 not in dict_chrom_ids and ref_id2 != -1):
                print str(ref_id1) + " " + str(ref_id2)
                #print str(read.reference_id) + " or " + str(read.next_reference_id) + ": not in " + str(dict_chrom_ids)
            else:
                #print ref_id1 + " " + ref_id2
                read.reference_id = tem.get_tid(dict_chrom_ids[ref_id1])
                read.next_reference_id = tem.get_tid(dict_chrom_ids[ref_id2]) if ref_id2 != -1 else -1
                out.write(read)
        print "Finished";
        out.close()
        bam.close()
        tem.close()
        print "Start to index the bam file";
        pysam.sort(options.prefix + ".bam", options.prefix + ".srt")

    def readChromInfo(self, options):
        """Read chrom info"""
        chrom_id = {}
        with open(options.chrom, 'r') as chrom:
            for line in chrom:
                print line
                line = line.rstrip()
                chrom_ids = line.split()
                #print chrom_ids
                chrom_id[chrom_ids[0]] = chrom_ids[1]
        return chrom_id
                

        

if __name__ == '__main__':
    parser = ArgumentParser(description="Rename chrom name")
    parser.add_argument('-b', "--bam", help="Input bam files", type=file, required=True)
    parser.add_argument('-t', "--template", help="Template bam files", type=file, required=True)
    parser.add_argument('-c', "--chrom", help="Chromosome information file", required=True)
    parser.add_argument('-p', "--prefix", help="Prefix of output bam file",  required=True)
    options = parser.parse_args()

    bam = Bam()
    bam.renameChrom(options)
