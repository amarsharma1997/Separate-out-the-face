import os
import face_recognition
import sys
from shutil import copyfile


"""
	Instructions:-
	1. Create one folder(Input Folder) which has images of people for which we have to filter the image.
	2. Create one folder(Check Folder) which has images to be checked.
	3. Create one folder(Output Folder) where the matched images has to be stored.
"""

input_path=""
images_path=""
output_path=""

def is_image(file):
	if file[len(file)-4:]=='.jpg' or file[len(file)-4:]=='.png':
		return True
	return False


def get_list_of_all_files(path):
	return os.listdir(path)

def get_input_face_encodings():
	files = get_list_of_all_files(input_path)
	input_face_encodings = []
	for file in files:
		if is_image(file):
			image_file = face_recognition.load_image_file(input_path+"/"+file)
			input_face_encodings = input_face_encodings + face_recognition.face_encodings(image_file)
	return input_face_encodings


def compare_face_encodings(input_face_encodings):
	files = get_list_of_all_files(images_path)
	a= 0
	total = len(files)
	matched_list=[]
	for file in files:
		a +=1 
		sys.stdout.write(str(a)+" out of "+str(total)+'\r')
		sys.stdout.flush()
		if is_image(file):
			image_file = face_recognition.load_image_file(images_path+"/"+file)
			image_face_encodings = face_recognition.face_encodings(image_file)
			result = False
			for face_encoding in image_face_encodings:
				for input_encoding in input_face_encodings:
					if face_recognition.compare_faces([input_encoding],face_encoding)[0]==True:
						result = True
			if result == True:
				matched_list.append(file)
	print("Matched "+str(len(matched_list))+" out of "+str(len(files)))
	return matched_list

def store_all_images(matched_list):
	for file in matched_list:
		copyfile(images_path+"/"+file,output_path+'/'+file)

def take_inputs():
	global input_path
	global images_path
	global output_path
	input_path = raw_input("Give path to input folder")
	images_path = raw_input("Give path to check folder")
	output_path = raw_input("Give path to output folder")

take_inputs()
print("Scanning Input Faces...")
input_face_encodings = get_input_face_encodings()
print("Scanned all input Faces...")
print("Comparing faces...")
matched_list = compare_face_encodings(input_face_encodings)
print("Storing all the matched images...")
store_all_images(matched_list)