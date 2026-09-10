(function(){
  'use strict';
  function bindPreview(input){
    var targetId=input.getAttribute('data-image-input');
    if(!targetId)return;
    var target=document.getElementById(targetId);
    if(!target)return;
    input.addEventListener('change',function(){
      var file=input.files&&input.files[0];
      if(!file)return;
      if(!file.type.startsWith('image/'))return;
      var url=URL.createObjectURL(file);
      target.innerHTML='';
      var img=document.createElement('img');
      img.src=url;
      img.alt='Pré-visualização da imagem';
      img.onload=function(){URL.revokeObjectURL(url);};
      target.appendChild(img);
    });
  }
  document.addEventListener('DOMContentLoaded',function(){
    document.querySelectorAll('[data-image-input]').forEach(bindPreview);
  });
})();
