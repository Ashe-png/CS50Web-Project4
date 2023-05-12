document.addEventListener('DOMContentLoaded', () => {
    const editButtons = document.querySelectorAll('.editButtons');
    const likeButtons = document.querySelectorAll('.likeButtons');

    likeButtons.forEach((button) => {

        button.addEventListener('click',(event) => {
            event.preventDefault();
            const buttonId = button.id;
            let postId = buttonId.match(/\d+/g);
            if (button.value === 'like') {
                fetch(`addlike/${postId}`)
                .then(response => response.json())
                .then(result => {
                    let newlikecount=result.data;
                    console.log(result.message);
                    button.value = 'unlike';
                    button.className='likeButtons btn btn-danger mb-3';
                    let likecount = document.getElementById(`likeCount_${postId}`)
                    if (newlikecount > 1) {
                        likecount.innerHTML= `${newlikecount} Likes`;
                    } else if (newlikecount === 1) {
                        likecount.innerHTML= `${newlikecount} Like`;
                    } else {
                        likecount.innerHTML= `No Likes`;
                    }
                })
            } else {
                fetch(`removelike/${postId}`)
                .then(response => response.json())
                .then(result => {
                    let newlikecount=result.data;
                    console.log(result.message);
                    button.value = 'like';
                    button.className='likeButtons btn btn-outline-danger mb-3';
                    let likecount = document.getElementById(`likeCount_${postId}`)
                    if (newlikecount > 1) {
                        likecount.innerHTML= `${newlikecount} Likes`;
                    } else if (newlikecount === 1) {
                        likecount.innerHTML= `${newlikecount} Like`;
                    } else {
                        likecount.innerHTML= `No Likes`;
                    }                    
            
                })
            }

        })
    })

    editButtons.forEach((button) => {     
            
        // Add click event listener to the edit button
        button.addEventListener('click', (event) => {

            event.preventDefault()
            const buttonId = button.id;
            let postId = buttonId.match(/\d+/g);
            button.style.display='none';
            const csrfToken = button.dataset.csrf;
            const contentElement = document.getElementById(postId) ;
        
            // Store the initial content
            const initialContent = contentElement.innerHTML;
           
            const textarea = document.createElement('textarea');
            textarea.className='create-field';
    
            // Set the textarea's value to the current content
            textarea.value = contentElement.innerHTML;
    
            // Replace the content element with the textarea
            contentElement.innerHTML = '';
            contentElement.appendChild(textarea);
    
            // create cancel button
            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Cancel';
            cancelButton.classList.add('btn', 'btn-danger', 'mb-3');

            let parentElement = button.parentNode;
            parentElement.appendChild(cancelButton);

            //create submit button
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save';
            saveButton.classList.add('btn', 'btn-primary', 'mx-3', 'mb-3');

            parentElement.appendChild(saveButton);

            // Add click event listener to the cancel button
            cancelButton.addEventListener('click', function() {
                button.style.display='';
                
                // Replace the textarea with the content element
                contentElement.innerHTML = initialContent;
                textarea.remove();
                // Remove the cancel button
                cancelButton.remove();
                saveButton.remove();
            });

            // Add click event listener to the submit button
            saveButton.addEventListener('click', (event) => {
                event.preventDefault()
                const textareaValue = textarea.value
                url = `edit/${postId}`
                fetch(url, {
                    method:"POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken                         
                    },
                    body: JSON.stringify({
                        content: textareaValue
                    })
                })
                .then(response => response.json())
                .then(result => {

                    newContent = result.data;
                    displayMessage(result.message, buttonId);
                    contentElement.innerHTML = newContent;
                    button.style.display='';
                    textarea.remove();
                    cancelButton.remove();
                    saveButton.remove();
                })

            });
            return false;
        });
    });


})



function displayMessage(message, buttonId) {
    // Create the message container dynamically
    let element = document.getElementById(buttonId).parentNode.parentNode.parentNode
    let element2 = document.getElementById(buttonId).parentNode.parentNode
    let messageContainer = document.createElement('p');
    messageContainer.id = 'message-container';
    messageContainer.style.display = 'flex'
    messageContainer.style.transform = 'translate(-50%, -50%)';
    messageContainer.style.padding = '5px 20px';
    messageContainer.style.borderRadius = '5px';
    messageContainer.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.2)';
    
    if (message === 'Post Edited Successfully.') {
        messageContainer.style.backgroundColor = '#8e43ed';
    }
    else {
        messageContainer.style.backgroundColor = '#f0ad4e';
        messageContainer.style.color = 'black';
    }
    // Create the message element
    let messageElement = document.createElement('p');
    messageElement.id = 'message';
    messageElement.style.margin = '0';
    messageElement.textContent = message;
  
    // Append the message element to the container
    messageContainer.appendChild(messageElement);
  
    // Append the container to the document body
    element.appendChild(messageContainer);
    element.insertBefore(messageContainer, element2);
  
    // Remove the message container after 3 seconds
    setTimeout(function() {
        // Add a CSS class to trigger the fade-out animation
        messageContainer.classList.add('fade-out');
        
        // Remove the message container after the animation ends
    setTimeout(function() {
        element.removeChild(messageContainer);
    }, 1000);
    }, 1000);
}

