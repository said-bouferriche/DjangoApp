const usernameField=document.querySelector('#usernameField');
const feedBackArea=document.querySelector('.invalid-feedback');
usernameField.addEventListener("keyup", (e)=>{
    console.log('ééé',222);
    const usernameValue = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display='none';

    if (usernameValue.length > 0){
        fetch('/authentification/validate-username', {
            body:JSON.stringify({username: usernameValue}),
            method: "POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log('data',data);
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