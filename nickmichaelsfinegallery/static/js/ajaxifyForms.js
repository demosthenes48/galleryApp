        $( document ).ready(function() {
            $(".tab").removeClass("active");
            $("#artistsTab").addClass("active");
        });


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
			closeDialog ();
		};

        function createCancelClicked () {
			$('#createArtistModal').modal('hide');
			$('#createFormMessage').hide();
			clearForm($('#createArtistForm'));
		};

		function editSaveClicked () {
			$('#editArtistForm').submit();
			closeDialog ();
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
			closeDialog ();
		};


        //generic showResponse and clearForm functions
        function showResponse(responseText, statusText, xhr, $form)  {
            $form.find('.successMessage').show();
            setTimeout(function(){
									$form.closest('.modal').modal('hide');
									$form.find('.successMessage').hide();
                                    clearForm($form);
                                 }, 3000);
        }

		function clearForm (form) {
			form.find("input[type=text], textarea").val("");
			clearCreateForm();
		};


        //pass parameters to modals
		$(document).on("click", ".open-deleteArtistModal", function () {
             var myDeleteArtistID = $(this).data('id');
             $("#deleteArtistKey").val(myDeleteArtistID);
        });

        $(document).on("click", ".open-editArtistModal", function () {
             var myEditArtistID = $(this).data('id');
             $("#deleteArtistKey").val(myDeleteArtistID);
             console.log($("#deleteArtistKey").val());
        });

        function fillEditModalDefaults(key, firstName, lastName, biography, photoName){
            biography = biography.replace(/\r?\n/g, "<br />");
            $("#editArtistKey").val(key)
            $("#editFirstName").val(firstName)
            $("#editLastName").val(lastName)
            $("#editBiography").val(biography)
            $("#editPhotoName").val(photoName)
        }