__author__ = 'WinterIsComing'

from ClusterResult2ProbabilityResult import *

# os.chdir('..')
#
# path = os.getcwd()

# cluster_file_2_frames(path)
# generate_probability_vector_result()
if __name__ == "__main__":
    # input_path = sys.argv[1]
    # output_path = sys.argv[2]
    # split_cluster_file(input_path, output_path)
    split_parse_generate(sys.argv[1], sys.argv[2])