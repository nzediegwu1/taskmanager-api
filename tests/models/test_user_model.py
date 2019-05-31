from src.models.user import User


class TestUserModel:
    def test_user_model_save_success(self, init_db, new_user):
        raised = False
        try:
            new_user.save()
        except:
            raised = True
        # if exception was not raised, save was successful
        assert not raised

    def test_user_model_get_succeeds(self):
        name = 'Anaeze Nsoffor'
        user = User.find_one(name=name)
        assert user.name == name
