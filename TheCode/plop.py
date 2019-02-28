#!/usr/bin/env python3

from os import cpu_count, path
import multiprocessing as mp
from math import ceil
from random import shuffle
from copy import deepcopy
import argparse


FILE_NAMES = ["../TheProblem/a_example.txt", "../TheProblem/b_lovely_landscapes.txt", "../TheProblem/c_memorable_moments.txt", "../TheProblem/d_pet_pictures.txt", "../TheProblem/e_shiny_selfies.txt"]
OUTPUT_PATH = "../TheOutput/"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default=FILE_NAMES[2], help=f"File to use as sample. Default is '{FILE_NAMES[2]}'")
parser.add_argument("-a", "--attempts", type=int, default=10, help="Attempts to create slideshow. The higher the number, the slower the process but the better the result. Default is 10")
args = parser.parse_args()

FILE_NAME = args.file
ATTEMPTS = args.attempts


def loadImagesFromFile(filePath):
    print(f"Loading {filePath}...")
    with open(filePath, "r") as file:
        r = file.read().split("\n")
    imgs = [(i, line.split()) for i, line in enumerate(r[1:]) if len(line) > 0]
    #print("File Loaded")
    return imgs

def createSlideshow(imgs):
    #print("Creating Slideshow...")
    slideshow = []
    usedImgs = set()
    done = False
    while not done:
        slide = [[], []]
        for id, img in imgs:
            if id not in usedImgs:
                usedImgs.add(id)
                slide[0].append(id)
                slide[1].extend(img[2:])
                break
        else:
            done = True
            break
        if img[0] == "V":
            for id2, img2 in imgs:
                if id2 not in usedImgs and img2[0] == "V":
                    usedImgs.add(id2)
                    slide[0].append(id2)
                    slide[1].extend(img2[2:])
                    break
            else:
                done = True
                break
        slide[1] = list(set(slide[1]))
        slideshow.append(slide)
    resultSlideshow.extend(slideshow)
    #print("Slideshow Created")
    return slideshow
        
def saveSlideshowToFile(slideshow, filePath):
    #print("Saving Slideshow...")
    success = False
    fileName = path.basename(filePath)
    with open(OUTPUT_PATH + fileName, "w") as file:
        file.write(f"{len(slideshow)}\n")
        for slide in slideshow:
            file.write(f"{' '.join([str(n) for n in slide[0]])}\n")
        success = True
    if not success:
        print("Problem occured while saving slideshow")

def calculateInterest(slideshow, i, j):
    list1 = slideshow[i][1]
    list2 = slideshow[j][1]
    set1 = set(list1)
    set2 = set(list2)
    common = len(set1 & set2)
    score = min(len(list1) - common, common, len(list2) - common)
    return score

def calculateScore(slideshow):
    score = 0
    for i in range(len(slideshow) - 1):
        score += calculateInterest(slideshow, i, i + 1)
    return score


def main():
    global resultSlideshow

    man = mp.Manager()
    bestSlideshow = []
    bestScore = -1
    cores = cpu_count()
    print(f"Running with {cores} cores...")
    imgs = loadImagesFromFile(FILE_NAME)
    magicNum = 64
    for a in range(ATTEMPTS):
        print(f"Attempt no. {a+1}:")
        resultSlideshow = man.list()
        processes = []
        shuffle(imgs)
        if len(imgs) < magicNum * cores:
            createSlideshow(imgs)
        else:
            n = ceil(len(imgs)/cores)
            #"""
            for i in range(cores):
                processes.append(mp.Process(target = createSlideshow, args = (imgs[n * i:n * (i+1)],)))
            for process in processes:
                process.start()
            for process in processes:
                process.join()
        score = calculateScore(resultSlideshow)
        print(f"Score: {score}\n")
        if score > bestScore:
            bestScore = score
            bestSlideshow = deepcopy(resultSlideshow)
            print(f"Bestscore: {bestScore}\n")
            saveSlideshowToFile(bestSlideshow, FILE_NAME[:FILE_NAME.index(".txt")] + "-output.txt")


if __name__ == "__main__":
    main()