# -*- coding: UTF-8 -*-
import sys

def replacefile(origin_filepath, new_filepath):
    with open(origin_filepath, 'w') as origin:
        with open(new_filepath, 'r') as new:
            for line in new.readlines():
                origin.write(line)

def main():
    origin_filepath = "C:/Users/10449/.neo4j/known_hosts"
    new_filepath = "C:/Users/10449/.neo4j/known_hosts_gqy"
    replacefile(origin_filepath, new_filepath)

if __name__ == "__main__":
    main()		