import axios from 'axios'

const API_URL = process.env.API_URL

const encounters = [
{
    'id': '1',
    'name': 'Reckoning',
    'gameSystem': 'dnd5e',
    'participants': [

    ]
}
]

export function fetchEncounters() {
return new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve(encounters)
    }, 300)
})
}

export function fetchSurveys() {
    return axios.get(`${API_URL}/surveys/`)
}

export function fetchSurvey(surveyId) {
    return axios.get(`${API_URL}/surveys/${surveyId}/`)
}

export function saveSurveyResponse(surveyResponse) {
    return axios.put(`${API_URL}/surveys/${surveyResponse.id}/`, surveyResponse)
}

export function postNewSurvey(survey, jwt) {
    return axios.post(`${API_URL}/surveys/`, survey, {
        headers: { Authorization: `Bearer ${jwt}` },
    })
}

export function authenticate(userData) {
    return axios.post(`${API_URL}/login/`, userData)
}

export function register(userData) {
    return axios.post(`${API_URL}/register/`, userData)
}
