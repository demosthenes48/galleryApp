    //generate create, edit, and delete ajax forms

        //artist forms

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


        //category forms

        $('#createCategoryForm').ajaxForm({
            target: '#createCategoryFormMessage',
            success: showResponse
        });

        $('#editCategoryForm').ajaxForm({
            target: '#editCategoryFormMessage',
            success: showResponse
        });

        $('#deleteCategoryForm').ajaxForm({
            target: '#deleteCategoryFormMessage',
            success: showResponse
        });


    //manage button clicks for modals

        //Artist button clicks

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


        //Category button clicks

        function createCategoryOKClicked () {
			$('#createCategoryForm').submit();
		};

        function createCategoryCancelClicked () {
			$('#createCategoryModal').modal('hide');
			$('#createCategoryFormMessage').hide();
			clearForm($('#createCategoryForm'));
		};

		function editCategorySaveClicked () {
			$('#editCategoryForm').submit();
		};

		function editCategoryCancelClicked () {
			$('#editCategoryModal').modal('hide');
			$('#editCategoryFormMessage').hide();
			clearForm($('#editCategoryForm'));
		};

		function deleteCategoryCancelClicked () {
			$('#deleteCategoryModal').modal('hide');
			$('#deleteCategoryFormMessage').hide();
			clearForm($('#deleteCategoryForm'));
		};

		function deleteCategoryDeleteClicked () {
			$('#deleteCategoryForm').submit();
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
                                    }else if (formID=="createCategoryForm" || formID=="editCategoryForm" || formID=="deleteCategoryForm"){
                                        $('#categoryTableBody').load('/admin/categories/refresh');
                                    }

                                 }, 3000);
        }

		function clearForm (form) {
			form.find("input[type=text], textarea").val("");
		};


    //pass parameters to modals

        //Artist modals

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


        //Category modals

		$(document).on("click", ".open-deleteCategoryModal", function () {
             var myDeleteCategoryID = $(this).data('id');
             $("#deleteCategoryKey").val(myDeleteCategoryID);
        });

        function fillCategoryEditModalDefaults(key, categoryName, photoName){
            $("#editCategoryKey").val(key)
            $("#editCategoryName").val(categoryName)
            $("#editCategoryPhotoName").val(photoName)
        }