        //generate create, edit, and delete ajax forms

        $('#createArtistForm').ajaxForm({
            target: '#createFormMessage',
            success: showResponse
        });

        $('#editArtistForm').ajaxForm({
            target: '#editFormMessage',
            success: showResponse
        });

        $('#deleteArtistForm').ajaxForm({
            target: '#deleteFormMessage',
            success: showResponse
        });


         //manage button clicks for modals

        function createOKClicked () {
			$('#createArtistForm').submit();
		};

        function createCancelClicked () {
			$('#createArtistModal').modal('hide');
			$('#createFormMessage').hide();
			clearForm($('#createArtistForm'));
		};

		function editSaveClicked () {
			$('#editArtistForm').submit();
		};

		function editCancelClicked () {
			$('#editArtistModal').modal('hide');
			$('#editFormMessage').hide();
			clearForm($('#editArtistForm'));
		};

		function deleteCancelClicked () {
			$('#deleteArtistModal').modal('hide');
			$('#deleteFormMessage').hide();
			clearForm($('#deleteArtistForm'));
		};

		function deleteDeleteClicked () {
			$('#deleteArtistForm').submit();
		};


        //generic showResponse and clearForm functions

        function showResponse(responseText, statusText, xhr, $form)  {
            $form.find('.successMessage').show();
            setTimeout(function(){
									$form.closest('.modal').modal('hide');
									$form.find('.successMessage').hide();
                                    clearForm($form);

                                    //update the appropriate form
                                    formID = $form.attr('id');
                                    if (formID=="createArtistForm" || formID=="editArtistForm" || formID=="deleteArtistForm"){
                                        $('#artistTableBody').load('/admin/artists/refresh');
                                    }

                                 }, 3000);
        }

		function clearForm (form) {
			form.find("input[type=text], textarea").val("");
		};

        function updateArtistTable () {

        };

        //pass parameters to modals

		$(document).on("click", ".open-deleteArtistModal", function () {
             var myDeleteArtistID = $(this).data('id');
             $("#deleteArtistKey").val(myDeleteArtistID);
        });

        function fillEditModalDefaults(key, firstName, lastName, biography, photoName){
            biography = biography.replace(/\r?\n/g, "<br />");
            $("#editArtistKey").val(key)
            $("#editFirstName").val(firstName)
            $("#editLastName").val(lastName)
            $("#editBiography").val(biography)
            $("#editPhotoName").val(photoName)
        }