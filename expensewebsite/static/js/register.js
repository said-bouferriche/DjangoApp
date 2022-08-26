const usernameField=document.querySelector('#usernameField');
const feedBackArea=document.querySelector('.invalid-feedback');
const EmailFeedbackErea=document.querySelector('.emailfeedbackArea');
const emailField=document.querySelector('#emailField');
const usernameSuccessOutput=document.querySelector('.usernameSuccessOutput');
const showPasswordToggle=document.querySelector('.showPasswordToggle');
const passwordField = document.querySelector("#passwordField");

usernameField.addEventListener("keyup", (e)=>{
    console.log('ééé',222);
    const usernameValue = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display='none';
    usernameSuccessOutput.textContent=`Checking ${usernameValue}`;
    usernameSuccessOutput.style.display = "block";

    if (usernameValue.length > 0){
        fetch('/authentification/validate-username', {
            body:JSON.stringify({username: usernameValue}),
            method: "POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log('data',data);
        usernameSuccessOutput.style.display = "none";
        if(data.username_error){
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display='block';
            feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
        }
        // else if(data.username_valid){
        //     usernameField.classList.add("is-valid");
        // }
    });
    }
});


emailField.addEventListener("keyup", (e)=>{
    const emailValue = e.target.value;
    emailField.classList.remove("is-invalid");
    EmailFeedbackErea.style.display='none';

    if (emailValue.length > 0){
        fetch('/authentification/validate-email', {
            body:JSON.stringify({email: emailValue}),
            method: "POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log('data',data);
        if(data.email_error){
            emailField.classList.add("is-invalid");
            EmailFeedbackErea.style.display='block';
            EmailFeedbackErea.innerHTML=`<p>${data.email_error}</p>`;
        }
        // else if(data.username_valid){
        //     usernameField.classList.add("is-valid");
        // }
    });
    }
});

const handleToggleInput = (e) =>{
    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    }
    else{
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");

    }
};

showPasswordToggle.addEventListener('click', handleToggleInput);