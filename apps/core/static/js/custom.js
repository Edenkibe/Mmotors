

// wen we click on we open a detail of a demand to response it:
$(document).on('click', '.me', function(event){ 
    event.preventDefault();
    console.log('me');
      
    const button = event.currentTarget;           // le bouton cliqué
    const url = this.href;                      // URL du contenu
    
    const show_stat = button.querySelector('span.show_stat'); // class pour show le resultat
    
    axios.get(url)
        .then(response => {
            // Mise à jour the type
            show_stat.textContent =response.data.button_text;
            $(show_stat).fadeIn();
        })
        .catch(error => {
            if(error.response && error.response.status === 403){
                window.alert("Connecte-toi avant de changer la disponibilite !");
            } else {
                console.error("Une erreur est survenue :", error);
            }
        });
});


