import Vue from "vue";
import createAuth0Client from "@auth0/auth0-spa-js";

/** Define a default action to perform after authentication */
const DEFAULT_REDIRECT_CALLBACK = () =>
    // console.log("Using default redirect callback.");
    window.history.replaceState({}, document.title, window.location.pathname);


let instance;

/** Returns the current instance of the SDK */
export const getInstance = () => instance;

/** Creates an instance of the Auth0 SDK. If one has already been created, it returns that instance */
export const useAuth0 = ({
    onRedirectCallback = DEFAULT_REDIRECT_CALLBACK,
    redirectUri = window.location.origin,
    ...options
}) => {
    if (instance) return instance;

    // The 'instance' is simply a Vue object
    // console.log("Creating instance of Auth0 plugin object.");
    instance = new Vue({
        data() {
            return {
                loading: true,
                isAuthenticated: false,
                user: {},
                auth0Client: null,
                popupOpen: false,
                error: null
            };
        },
        methods: {
            /** Authenticates the user using a popup window */
            async loginWithPopup(o) {
                // console.log("Mark the popup opened");
                this.popupOpen = true;

                try {
                    // console.log("Open the popup");
                    await this.auth0Client.loginWithPopup(o);
                } catch (e) {
                    // eslint-disable-next-line
                    console.error(e);
                } finally {
                    // console.log("Mark the popup closed");
                    this.popupOpen = false;
                }

                this.user = await this.auth0Client.getUser();
                this.isAuthenticated = true;
            },
            /** Handles the callback when logging in using a redirect */
            async handleRedirectCallback() {
                // console.log("handleRedirectCallback");
                this.loading = true;
                try {
                    // console.log("Call client.handleRedirectCallback()");
                    await this.auth0Client.handleRedirectCallback();
                    // console.log("Get the user");
                    this.user = await this.auth0Client.getUser();
                    this.isAuthenticated = true;
                } catch (e) {
                    console.error(e);
                    this.error = e;
                } finally {
                    this.loading = false;
                }
            },
            /** Authenticates the user using the redirect method */
            loginWithRedirect(o) {
                // console.log("Login with redirect");
                return this.auth0Client.loginWithRedirect(o);
            },
            /** Returns all the claims present in the ID token */
            getIdTokenClaims(o) {
                console.log("Get ID token claims");
                return this.auth0Client.getIdTokenClaims(o);
            },
            /** Returns the access token. If the token is invalid or missing, a new one is retrieved */
            getTokenSilently(o) {
                // console.log("Get token silently");
                return this.auth0Client.getTokenSilently(o);
            },
            /** Gets the access token using a popup window */

            getTokenWithPopup(o) {
                // console.log("Get token with popup");
                return this.auth0Client.getTokenWithPopup(o);
            },
            /** Logs the user out and removes their session on the authorization server */
            logout(o) {
                // console.log("Logout");
                return this.auth0Client.logout(o);
            }
        },
        /** Use this lifecycle method to instantiate the SDK client */
        async created() {
            // Create a new instance of the SDK client using members of the given options object
            // console.log("Create Auth0 client");
            this.auth0Client = await createAuth0Client({
                domain: options.domain,
                client_id: options.clientId,
                audience: options.audience,
                redirect_uri: redirectUri
            });

            try {
                // If the user is returning to the app after authentication...
                // console.log("Check for 'code' and 'state' on return:", window.location);
                if (
                    window.location.search.includes("code=") &&
                    window.location.search.includes("state=")
                ) {
                    // console.log("Get state from redirect callback");
                    // handle the redirect and retrieve tokens
                    const { appState } = await this.auth0Client.handleRedirectCallback();

                    // Notify subscribers that the redirect callback has happened, passing the appState
                    // (useful for retrieving any pre-authentication state)
                    // console.log("Call onRedirectCallback() with state");
                    onRedirectCallback(appState);
                }
            } catch (e) {
                console.error(e);
                this.error = e;
            } finally {
                // Initialize our internal authentication state
                this.isAuthenticated = await this.auth0Client.isAuthenticated();
                this.user = await this.auth0Client.getUser();
                this.loading = false;
            }
        }
    });

    return instance;
};

// Create a simple Vue plugin to expose the wrapper object throughout the application
export const Auth0Plugin = {
    install(Vue, options) {
        // console.log("Installing Auth0 plugin");
        Vue.prototype.$auth = useAuth0(options);
    }
};
