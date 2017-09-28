import os
from datetime import date
import filecmp

#My work was done with the original files for this project. Only modification I
#made to the source code was changing the original 35 points of the first test to 40. 
def getData(file):
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys will come from the first row in the data.

#Note: The column headings will not change from the
#test cases below, but the the data itself will
#change (contents and size) in the different test
#cases.

	#Your code here:
	f = open(file,'r')
	next(f)
	headers = ["First","Last","Email","Class","DOB"]
	data_list = []


	for line in f:
		data_dict = {}
		for x,y in zip(headers,line.split(',')):
			if "\n" in y:
				y = y.replace("\n","")
			data_dict[x] = y

		data_list.append(data_dict)

	return data_list
#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName

	#Your code here:
	new_list = sorted(data,key = lambda x: x[col])
	return (new_list[0]["First"] + " " + new_list[0]["Last"])

#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	#Your code here:
	new_dict = {}
	for x in data:
		if x["Class"] not in new_dict.keys():
			new_dict[x["Class"]] = 1
		else:
			new_dict[x["Class"]] += 1

	new_list = sorted(new_dict.items(), key = lambda x: x[1] ,reverse = True)
	return new_list

# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	#Your code here:
	day_dict = {}
	for x in a:
		birth_day = x["DOB"].split("/")
		if birth_day[1] not in day_dict.keys():
			day_dict[birth_day[1]] = 1
		else:
			day_dict[birth_day[1]] += 1

	day = sorted(day_dict, key = lambda x: day_dict[x], reverse = True)[0]
	return int(day)

# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	#Your code here:
	today = date.today()
	age_list = []

	for x in a:
		birth_date = list(map(int, x["DOB"].split("/")))
		age = abs(today.year - birth_date[2] + (today.month - birth_date[1])/12 + (today.day - birth_date[0])/365)
		age_list.append(age)
	total = 0

	for age in age_list:
		total += age

	average_age = round(total/len(age_list))
	return average_age

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None

	#Your code here:
	new_list = sorted(a, key = lambda x: x[col])
	new_file = open(fileName, 'w')
	for x in new_list:
		new_file.write("{},{},{},\n".format(x["First"], x["Last"], x["Email"]))


	new_file.close()



################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)

	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()
