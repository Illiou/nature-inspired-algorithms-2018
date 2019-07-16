import unittest
import csv
import json
import os
from Final.Solution import Solution


class SolutionTest(unittest.TestCase):
    def test_save(self):
        tsp_solution = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0],
                        [0], [11, 15, 1, 8, 5, 0, 3, 4, 9, 12, 7, 13, 10,
                              14, 6, 2], [11, 8, 5, 13, 10, 9, 7, 1, 3, 4, 12, 6, 14,
                                             2, 15, 0], [0], [0], [0], [0], [0],
                        [19, 16, 7, 17, 1, 15, 0, 4, 5, 18, 8, 6, 3,
                         23, 11, 12, 13, 9, 25, 20, 21, 24, 14, 22, 2, 10], [0], [0], [0],
                        [29, 3, 24, 44, 35, 16, 38, 31, 7, 33, 2, 43, 32,
                         30, 12, 13, 17, 20, 42, 37, 15, 26, 5, 28, 0, 27,
                         8, 36, 40, 4, 9, 6, 1, 19, 45, 41, 25, 11, 18,
                         39, 21, 34, 10, 23, 22, 14], [0]]
        lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 948.0, 884.0, 0, 0, 0, 0, 0, 802.0, 0, 0,
                   0, 1492.0, 0]
        solution = Solution(tsp_solution, lengths)
        csv_filename = "./test_solution.tsv"
        json_filename = "./test_solution.json"
        solution.save(csv_filename)
        with open(csv_filename, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter="\t")
            rows = [row for row in reader]
            self.assertEqual("visited customers", rows[0][1])
            for row, tsp, length in zip(rows[1:], tsp_solution, lengths):
                self.assertEqual(eval(row[1]), tsp)
                self.assertEqual(eval(row[2]), length)
        solution.save(json_filename=json_filename)
        with open(json_filename, "r") as json_file:
            json_dump = json.load(json_file)
            self.assertEqual(dict, type(json_dump["per_vehicle"]))
            self.assertEqual(dict, type(json_dump["per_attribute"]))
            for i, (tsp, length) in enumerate(zip(tsp_solution, lengths)):
                if length == 0:
                    continue
                self.assertEqual(tsp, json_dump["per_vehicle"][f"vehicle_{i+1}"]["visited_customers"])
                self.assertEqual(length, json_dump["per_vehicle"][f"vehicle_{i+1}"]["driven_distance"])
        os.unlink(csv_filename)
        os.unlink(json_filename)

