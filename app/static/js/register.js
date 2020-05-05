const addMajors = () => {
    data = JSON.parse(data)
    for(var i = 0; i < data.length; i++) {
        console.log(i)
        $('#majors').append(
            `<option value="${data[i]}"/>`
        )
    }
}

const addYears = () => {
    years = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
    years.map((year) => {
        $('#years').append(
            `<option value="${year}"/>`
        )
    })
}

addMajors();
addYears();