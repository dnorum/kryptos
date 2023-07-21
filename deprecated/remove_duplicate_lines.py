outfilename = "key_autokey_patchwork_10kwords.output3"
infilename = "key_autokey_patchwork_10kwords.output"

lines_seen = set() 
outfile = open(outfilename, "w")
for line in open(infilename, "r"):
    if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
