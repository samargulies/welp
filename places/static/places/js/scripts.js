if( document.querySelector('.place-detail__images--extended') !== null ) {
	var flkty = new Flickity( '.place-detail__images--extended', {
		pageDots: false, 
		fullscreen: true, 
		initialIndex: 1,
		on: {
			staticClick: function( event, pointer, cellElement, cellIndex ) {
			  // dismiss if cell was not clicked
			    if ( !cellElement ) {
			      return;
			    }
			
			    flkty.select(cellIndex);
				flkty.toggleFullscreen();
			}
		}
	});
}

