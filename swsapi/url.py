class URLManager:
    """
    Classe pour gérer les URL et points de terminaison de l'API SoWeSign.
    """
    SOWESIGN_BASE_URL = "https://app.sowesign.com/api/"
    SOWESIGN_TOKEN_AUTHENTICATION_ENDPOINT = "portal/authentication/token"
    SOWESIGN_COURSES_ENDPOINT = "student-portal/courses"
    SOWESIGN_FUTURE_COURSES_ENDPOINT = "student-portal/future-courses"
    SOWESIGN_STUDENT_ENDPOINT = "student-portal"

    @classmethod
    def get_token_authentication_url(cls):
        """
        Retourne le point de terminaison API pour obtenir un jeton d'authentification.
        """
        return cls.SOWESIGN_BASE_URL + cls.SOWESIGN_TOKEN_AUTHENTICATION_ENDPOINT

    @classmethod
    def get_courses_url(cls):
        """
        Retourne le point de terminaison API pour la ressource 'courses'.
        """
        return cls.SOWESIGN_BASE_URL + cls.SOWESIGN_COURSES_ENDPOINT

    @classmethod
    def get_future_courses_url(cls):
        """
        Retourne le point de terminaison API pour la ressource 'future courses'
        """
        return cls.SOWESIGN_BASE_URL + cls.SOWESIGN_FUTURE_COURSES_ENDPOINT
