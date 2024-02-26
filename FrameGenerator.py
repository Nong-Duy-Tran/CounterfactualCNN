from helper_function import frames_from_video_file
import random

class Modified_Frame_Generator:
    def __init__(self, dataset_path, index_path, n_frames, training):
        """ Returns a set of frames with their associated label. 

        Args:
            dataset_path: A path reference to a .txt file that contain paths of multiple videos in each line.
            n_frames: Number of frames. 
            training: Boolean to determine if training dataset is being created.
            index_path: A path reference to a .txt file that has index number for each video class.
        """
        self.path = dataset_path
        self.n_frames = n_frames
        self.training = training
        
        self.class_index = self.generate_class_dictionary(index_path)



    def generate_class_dictionary(self, index_path):
        index_file = open(index_path, 'r')

        class_index = {}
        while True:
            line = index_file.readline()

            if not line:
                break

            index, class_name = line.split(' ')
            class_name = class_name.split('\n')[0]

            class_index[index] = class_name

        index_file.close()
        
        return class_index



    def video_path_dictionary(self):
        """ 
        Create a dictionary that has keys is path to a video, values is its encoded class
        """

        f = open(self.path, 'r')

        video_path = {}

        while True:
            line = f.readline()

            if not line:
                # print('EOF')
                break

            else:
                line = f.readline().split(' ')

            full_path = 'D:/Dataset/archive/UCF-101/' + line[0]

            video_path[full_path] = line[1].split('\n')[0]
        
        return video_path
    

    def __call__(self):
        path_dictionary = self.video_path_dictionary()

        '''
        video_path = list(path_dictionary.keys())
        class_of_video = list(self.class_index[i] for i in path_dictionary.values())
        
        print(class_of_video[:100])
        '''
        pairs = list(zip(path_dictionary.keys(), path_dictionary.values()))

        random.shuffle(pairs)

        for path, name in pairs:
            video_frames = frames_from_video_file(path, self.n_frames) 
            label = name
            yield video_frames, label