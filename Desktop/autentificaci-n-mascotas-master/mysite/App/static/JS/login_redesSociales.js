
// Firebase config
var firebaseConfig = {
    apiKey: "AIzaSyDODdAaKjeUDaLsfm-t-nFLBFFEPYjo44Y",
    authDomain: "autentificacion-de-animales.firebaseapp.com",
    databaseURL: "https://autentificacion-de-animales.firebaseio.com",
    projectId: "autentificacion-de-animales",
    storageBucket: "autentificacion-de-animales.appspot.com",
    messagingSenderId: "135378187853",
    appId: "1:135378187853:web:955a63790002c3fb4a4e04",
    measurementId: "G-L13XR3G9LB"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
auth.languageCode = 'en';  // Configurar idioma para Firebase Auth
const provider = new GoogleAuthProvider();

// Evento para el botón de Google Sign-In
const googleSignInButton = document.getElementById("googleSignIn");
googleSignInButton.addEventListener('click', async (e) => {
    e.preventDefault();
    
    try {
        const result = await signInWithPopup(auth, provider);
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential.accessToken;
        const user = result.user;

        console.log('User signed in: ', user);

        window.location.href = '/vistaPrinc/';
        
    } catch (error) {
        if (error.code === 'auth/popup-closed-by-user') {
            console.error('El usuario cerró la ventana emergente de inicio de sesión.');
        } else {
            console.error('Error signing in: ', error.message);
        }
    }
});



// Función para actualizar el perfil del usuario
function updateUserProfile(user) {
    if (user) {
        const userName = user.displayName;
        const userEmail = user.email;
        const userPhoto = user.photoURL;

        return {
            name: userName,
            email: userEmail,
            photo: userPhoto
        };
    } else {
        console.error('El objeto usuario no es válido.');
        return null;
    }
}


/* // Inicializa Firebase si no está ya inicializado
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
} else {
    firebase.app();
}
 */

/* // Obtener CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} */


/* // Ejemplo de cómo usar el token CSRF en una solicitud fetch
function enviarDatosAlServidor(payload) {
    const csrftoken = getCookie('csrftoken');  // Obtén el token CSRF

    fetch('/some-endpoint/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,  // Incluir el token CSRF en el encabezado
        },
        body: JSON.stringify(payload)  // Datos que envías al servidor
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
} */


/* // Función para iniciar sesión con Google
function googleSignIn() {
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithRedirect(provider);
} */


/* firebase.auth().getRedirectResult().then((result) => {
    if (result.user) {
        console.log("Usuario autenticado: ", result.user);
        // El usuario ha iniciado sesión, obtener el idToken
        result.user.getIdToken().then((idToken) => {
            console.log("ID Token: ", idToken);
            // Enviar el idToken al backend para la verificación
            fetch('/google_login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Aquí incluyes el token CSRF
                },
                body: JSON.stringify({ id_token: idToken })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = data.redirect_url;  // Redirige si todo fue exitoso
                } else {
                    console.error("Error en la autenticación en el backend:", data.message);
                }
            });
        });
    } else {
        console.error("No se pudo autenticar al usuario.");
        // Imprime el resultado completo para investigar
        console.log("Resultado de getRedirectResult(): ", result);
    }
}).catch((error) => {
    console.error('Error durante la autenticación con Google:', error);
}); */



// Función para iniciar sesión con Facebook
function loginFacebook() {
    const provider = new firebase.auth.FacebookAuthProvider();
    provider.addScope('email');
    provider.addScope('public_profile');
    auth.signInWithRedirect(provider);

    auth.getRedirectResult().then((result) => {
        if (result.credential) {
            const token = result.credential.accessToken;
            console.log("Facebook Access Token:", token);
        }
        const user = result.user;
        if (user) {
            console.log("Usuario autenticado con Facebook:", user);
            // Aquí también podrías enviar el token al backend si fuera necesario
        }
    }).catch((error) => {
        console.error("Error durante el login con Facebook:", error);
    });
}

// Función para iniciar sesión con GitHub
function loginGithub() {
    const provider = new firebase.auth.GithubAuthProvider();
    provider.addScope('email');
    provider.addScope('public_profile');
    auth.signInWithRedirect(provider);

    auth.getRedirectResult().then((result) => {
        if (result.credential) {
            const token = result.credential.accessToken;
            console.log("Github Access Token:", token);
        }
        const user = result.user;
        if (user) {
            console.log("Usuario autenticado con Github:", user);
            // Aquí también podrías enviar el token al backend si fuera necesario
        }
    }).catch((error) => {
        console.error("Error durante el login con Github:", error);
    });
}
