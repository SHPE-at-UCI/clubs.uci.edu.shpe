const functions = require('firebase-functions');

// Create and Deploy Your First Cloud Functions
// https://firebase.google.com/docs/functions/write-firebase-functions

exports.helloWorld = functions.https.onRequest((request, response) => {
 response.send("Hello from Firebase!");
});


exports.majors = functions.https.onRequest((request, response) => {
    allMajors = ['Aerospace Engineering', 'African American Studies', 'Anthropology', 'Applied Physics', 'Art', 'Art History', 'Asian American Studies', 'Biochemistry and Molecular Biology', 'Biological Sciences', 'Biology/Education', 'Biomedical Engineering', 'Biomedical Engineering: Premedical', 'Business Administration', 'Business Economics', 'Business Information Management', 'Chemical Engineering', 'Chemistry', 'Chicano/Latino Studies', 'Chinese Studies', 'Civil Engineering', 'Classics', 'Cognitive Sciences', 'Comparative Literature', 'Computer Engineering', 'Computer Game Science', 'Computer Science', 'Computer Science and Engineering', 'Criminology', 'Dance', 'Data Science', 'Developmental and Cell Biology', 'Drama', 'Earth System Science', 'East Asian Cultures', 'Ecology and Evolutionary Biology', 'Economics', 'Education Sciences', 'Electrical Engineering', 'Engineering', 'English', 'Environmental Engineering', 'Environmental Science and Policy', 'European Studies', 'Exercise Sciences', 'Film and Media Studies', 'French', 'Gender and Sexuality Studies', 'Genetics', 'German Studies', 'Global Cultures', 'Global Middle East Studies', 'History', 'Human Biology', 'Informatics', 'International Studies', 'Japanese Language and Literature', 'Korean Literature and Culture', 'Language Science', 'Literary Journalism', 'Materials Science and Engineering', 'Mathematics', 'Mechanical Engineering', 'Microbiology and Immunology', 'Music', 'Neurobiology', 'Nursing Science', 'Pharmaceutical Sciences', 'Philosophy', 'Physics', 'Political Science', 'Psychology', 'Psychological Science', 'Public Health Sciences', 'Quantitative Economics', 'Religious Studies', 'Social Ecology', 'Social Policy and Public Service', 'Sociology', 'Software Engineering', 'Spanish', 'Urban Studies']
    response.send(JSON.stringify(allMajors))
});