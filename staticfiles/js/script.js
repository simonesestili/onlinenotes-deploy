var titleInputClasses = document.querySelector('#id_title').classList;
titleInputClasses.add('form-control');
titleInputClasses.add('form-control-lg');
titleInputClasses.add('my-5');

var contentInputClasses = document.querySelector('#id_content').classList;
contentInputClasses.add('form-control');

var titleInput = document.querySelector('#id_title');

if (titleInput.value === 'Untitled Note' || titleInput.value === ''){
    titleInput.placeholder = 'Untitled Note';
    titleInput.required = false;
    titleInput.value = null;
}