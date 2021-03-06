
# gradescope-scripts
These scripts are written to prepare student submissions as downloaded from CourseWeb to be uploaded to GradeScope for the purposes of
* automatic or manual grading [1,3,4]
* plagiarism detection [2]

## Getting Started

### Prerequisites
* Python  - [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Python requests library 

		$ python -m pip install requests

### Setting Up
* Clone this repository to a suitable location e.g.`~/gs`
* Unzip the student submissions into a folder e.g. `~/gs/submissions`

	> The student submissions should be in the format of:
	> `~/gs/submissions/<batch>/<student-details>/<student-id>.zip`

### Running
* Login to GradeScope, open your course, then assignment, and note the _course-id_ and _assignment-id_ by the browser URL displayed
	> `gradescope.com/courses/<course-id>/assignment/<assignment-id>` 

* Run the script **clean-all.py** using the following command:

		 $ python clean-all.py ~/gs/submissions

* The script will creates a CSV file `students.csv`. This could be used to bulk-upload students to GradeScope using the interface provided at:
	> ` gradescope.com/courses/<course-id>/memberships `

* The submissions should now be re-organised into the following format
	> ` ~/gs/submissions/<student-id>/<student-id>.java `
The `<student-id>.java` contains a merged version of all the source files belonging to the student. This yields more accurate similarity comparisons between code for plagiarism detection with less false positives.

* Upload the submissions to GradeScope using the script **upload-all.py** from within the `submissions` folder

		$ cd submissions
		$ python ../upload-all.py 

## What Happens
This is an abstract explanation of what the program does. In-depth details could be understood by readingv the code
* clean-all.py
	1. Traverse the submission folder hierarchy and generate the student list as CSV
	1. Moves all the student submission folders from inside batch folders to the submission root e.g. from `~/gs/submissions/<batch>/<student-submission>` to `~/gs/submissions/<student-submission>`
	1. The student submission folder names are a combination of names and student-ids, rename these to just student-ids
	1. Recursively extract all the zip files found inside the folder hierarchy. This includes zips inside zips as well
	1. Recursively remove all non-source files - at the moment we assume source is contained inside **.java** or **.txt** files only. Unfortunately if students have put source files in other formats such as WORD or PDF, they'll be removed too. This also renames all .txt extensions to .java extensions.
	1. Move all source files to the student-submission root e.g. directly under `~/gs/submissions/<student-id>`
	1. Removes all empty folders
	1. Lists all student submissions with no files in them - this means all the files inside them were removed due to reasons mentioned above
	1. if `merge==True` merges all the source files inside each student submission folder into one source file. This helps when comparing submissions during plagiarism checking, and yields better results.
	
* upload-all.py
	1. Logs into GradeScope using given credentials
	1. Captures the course-id and assignment-id from the user
	1. Loops through all the student folders
	1. For each student folder, uploads the student submission to the given course/assignment using HTTP post requests
	
## Notes
The merge feature could be turned off by:
* setting `merge = False` in upload-all.py, and
* commenting out the function call to `merge_files()` in clean-all.py 

This will result in multiple source files inside the student folder within `submissions`
 > `~/gs/submissions/<student-id>/[files]`

## Limitations
* Supports extraction of  only **zip**, **jar**, and **rar** files in the submission hierarchy
* Students' source code should be included within **.java** or **.txt** files, any files without extensions will be removed, along with any code written inside word or PDF documents
* Limited to the  folder hierarchy structure of CourseWeb only. Generalising this would require rewriting a significant part of the code
* Limited to the CSV format specified by GradeScope
* Limited to JAVA coding assignments - this can be generalised easily to other languages

## Future Work
The following items are in the development pipeline
* Migrate all code to python3
* Instead of modifying the existing submissions folder, work the changes on a deep copy
* Replace calls to `subprocess` with suitable python libraries
* Use inner functions where possible - e.g. for recursive operations
* Generalising to a wider set of courses, assignments, and submissions
	* configurable folder structures
	* configurable filtering parameters for source code (e.g. **.c,** **.py,** etc.)
* Support more zip file formats 
	* e.g. **.7z**, **.tar.gz**
* Support more filetypes where source code might reside in
	* e.g. **.docx**, **.pdf**, screenshots (using OCR), etc. 
* Configurations via command line arguments to run parts of the code
	* E.g. allow the user to run cleanup steps 1,2,5, skipping 3,4

## Credits | References
* [0] Olga Sadie, Customer Happiness Manager at GradeScope
* [1] [https://www.gradescope.com/help#help-center-item-programming-assignments](https://www.gradescope.com/help#help-center-item-programming-assignments)
* [2] [https://www.gradescope.com/help#help-center-item-programming-assignments-review-similarity](https://www.gradescope.com/help#help-center-item-programming-assignments-review-similarity)
* [3] [https://gradescope-autograders.readthedocs.io/en/latest/specs/](https://gradescope-autograders.readthedocs.io/en/latest/specs/)
* [4] [https://gradescope-autograders.readthedocs.io/en/latest/manual_grading/](https://gradescope-autograders.readthedocs.io/en/latest/manual_grading/)
