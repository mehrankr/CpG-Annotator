from argparse import ArgumentParser
import gzip


def get_args():
    parser = ArgumentParser(
        description="Used a 4 column "
        "CpG island annotated bed files and creates "
        "an expanded annotation with shores, shelves "
        "and resorts.")
    parser.add_argument(
        "in_path",
        help="Path to 4 column bed file of CpG "
        "island annotations. This can be obtained "
        "from ucsc genome browser.")
    parser.add_argument(
        "out_path",
        help="Full path to output extended bed file")
    parser.add_argument(
        "-gzip_io",
        action="store_true",
        help="Input and output would be gzipped")
    args = parser.parse_args()
    return args


class AnnotateLine:
    def __init__(self, cpg_line):
        self.cpg_list = cpg_line.rstrip().split("\t")
        self.start, self.end = [int(each) for each in self.cpg_list[1:3]]
        self.chr = self.cpg_list[0]
        self.cpg_name = self.cpg_list[3]
        self.out_list = self.expand_cpg()

    def expand_cpg(self):
        shore_down = [self.chr, self.start - 2000,
                      self.start,
                      "{}.S.Shore".format(self.cpg_name)]
        shore_up = [self.chr, self.end,
                    self.end + 2000,
                    "{}.N.Shore".format(self.cpg_name)]
        shelf_down = [self.chr, self.start - 4000,
                      self.start - 2000,
                      "{}.S.Shelf".format(self.cpg_name)]
        shelf_up = [self.chr, self.end + 2000,
                    self.end + 4000,
                    "{}.N.Shelf".format(self.cpg_name)]
        resort = [self.chr, self.start - 4000,
                  self.start + 4000,
                  "{}.Resort".format(self.cpg_name)]
        out_list = [shore_down, shore_up, shelf_down,
                    shelf_up, resort]
        return out_list


def annotate_cpg(in_path, out_path, gzip_io):
    if gzip_io:
        in_link = gzip.open(in_path, "rb")
        out_link = gzip.open(out_path, "wb")
    else:
        in_link = open(in_path, "r")
        out_link = open(out_path, "w")
    for cpg_line in in_link:
        CpgObj = AnnotateLine(cpg_line)
        out_link.write(cpg_line)
        for each_list in CpgObj.out_list:
            if each_list[1] > 0:
                # Making sure the start is a valid position
                out_str = "\t".join([str(each_item) for each_item
                                     in each_list]) + "\n"
                out_link.write(out_str)
    out_link.close()
    in_link.close()


if __name__ == "__main__":
    args = get_args()
    annotate_cpg(args.in_path, args.out_path,
                 args.gzip_io)
