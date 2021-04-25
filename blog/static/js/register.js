

const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.invalid_email_feedback');
const emailSuccessOutput = document.querySelector('.emailSuccess');
const showPasswordToggle =document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector('#passwordField');
const btnSubmit = document.querySelector('.btn-submit');

const handleToggleInput = (e)=>{
    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type","text");

    }else{
        showPasswordToggle.textContent ="SHOW";
        passwordField.setAttribute("type","password");
    }
}
showPasswordToggle.addEventListener('click', handleToggleInput);
emailField.addEventListener('keyup', (e) =>{
    const emailVal = e.target.value;
    emailSuccessOutput.textContent = `checking ${emailVal}`

    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display ='none';

    if(emailVal.length>0){

        fetch('/authentication/validate-email',{
            body:JSON.stringify({email:emailVal}),
            method: "POST",
        }).then((res) => res.json())
        .then((data)=>{
            // console.log('data',data);
            emailSuccessOutput.style.display ='block';

            if(data.email_error){
                // displaying the error
                btnSubmit.disabled = true;
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display ="block";
                emailFeedbackArea.innerHTML =`<p>${data.email_error}</p>`;

            }else{
                btnSubmit.removeAttribute("disabled");
            }

        });
    }



});




const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid_feedback');
const usernameSuccessOutput = document.querySelector('.usernameSuccess');
usernameField.addEventListener('keyup',(e) =>{
    console.log('77777',77777);
    const usernameVal = e.target.value;
    console.log('usernameVal',usernameVal );
    usernameSuccessOutput.textContent = `checking ${usernameVal}`;

    // hiding the error when everything is okay
    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display ="none";
    
    if(usernameVal.length>0){
        fetch('/authentication/validate-username',{
            body:JSON.stringify({username:usernameVal}),
            method: "POST",
        }).then((res) => res.json())
        .then((data) =>{
            console.log('data',data);
            usernameSuccessOutput.style.display ='block';

            if(data.username_error){
                btnSubmit.disabled = true;
               
                // displaying the error
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display ="block";
                feedbackArea.innerHTML =`<p>${data.username_error}</p>`;
            }
            else{
                btnSubmit.removeAttribute("disabled");
            }
        });

    }
   
});