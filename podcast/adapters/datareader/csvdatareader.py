import os
import csv
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    # TODO: Complete the implementation of the CSVDataReader class.
    def __init__(self, podcast_filename:str, episode_filename:str):
        self.podcast_list = []
        self.episode_list = []
        self.category_set = set()
        self.author_set = set()

        podcast_file = open(podcast_filename, 'r', encoding='utf-8-sig')
        podcast_lines = csv.reader(podcast_file)
        # skip the first line(header)
        headers = next(podcast_lines)
        for line in podcast_lines:
            '''
            csv:id(0), title(1), image(2), description(3), language(4), categories(5), website(6), author(7), itunes_id(8)
            podcast(id(0), author(7), title(1), image(2), description(3), website(6), itunes_id(8), language(4))
            '''
            try:
            # create a author object and add it to the set
            # use the current author set length to create an unique id for each author
            # if a podcast's author doesn't exist, don't add that podcast
                author = Author(len(self.author_set) + 1, line[7])
                podcast = Podcast(int(line[0]), author, line[1], line[2], line[3], line[6], int(line[8]), line[4])
                author.add_podcast(podcast)
                self.author_set.add(author)
                self.podcast_list.append(podcast)
                # categories are divided by | use split to get each category
                categories = line[5].split("|")
                # go through every category of a podcast
                # create a category object and add it to the set and the corresponding podcast
                for category in categories:
                # use the current category set length to create an unique id for each category
                    c = Category(len(self.category_set) + 1, category)
                    self.category_set.add(c)
                    podcast.add_category(c)
            except:
                pass
        podcast_file.close()

        episode_file = open(episode_filename, 'r', encoding='utf-8-sig')
        episode_lines = csv.reader(episode_file)
        # skips the first line(header)
        headers = next(episode_lines)
        for line in episode_lines:
            '''
            csv:id,podcast_id,title,audio,audio_length,description,pub_date
            episode_id: int, podcast: Podcast, title: str, audio:str length: int, description: str, pub_date: str
            '''
            # check if a podcast with the podcast id of an episode exists in the podcast list
            # if it does, get that podcast object and create an episode object with it
            podcast_id = int(line[1])
            podcast_index = -1
            for i in range(len(self.podcast_list)):
                if self.podcast_list[i].id == podcast_id:
                    podcast_index = i
            # only when the podcast of an episode is found, add that episode to the list
            # since an episode without a podcast can't exist
            if podcast_index != -1:
                episode_podcast = self.podcast_list[podcast_index]
                episode = Episode(int(line[0]), episode_podcast, line[2], line[3], int(line[4]), line[5], line[6])
                episode_podcast.add_episode(episode)
                self.episode_list.append(episode)
        episode_file.close()







