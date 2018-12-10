//imports
import {actionCreators as UserActions} from "redux/modules/user";

//actions
const SET_NEWS = "SET_NEWS";
const SET_PWORD = "SET_PWORD";
const SET_NPWORD = "SET_NPWORD";
function setNews(news) {
    return {
        type: SET_NEWS,
        news
    }
}
function setPword(pword) {
    return {
        type: SET_PWORD,
        pword
    }
}
function setNPword(npword) {
    return {
        type: SET_NPWORD,
        npword
    }
}
function getNews(Time) {
    console.log(Time)
    const url = "/news/search/?time=" + Time
    console.log(url)
    return (dispatch, getState) => {
        fetch(url)
            .then(response => response.json())
            .then(json => {
                console.log(json)
                dispatch(setNews(json))
            });
    }
}
function getPword(Time) {
    console.log(Time)
    const url = "/news/pgword/?time=" + Time
    console.log(url)
    return (dispatch, getState) => {
        fetch(url)
            .then(response => response.json())
            .then(json => {
                console.log(json)
                dispatch(setPword(json))
            });
    }
}
function getNPword(Time) {
    console.log(Time)
    const url = "/news/npgword/?time=" + Time
    console.log(url)
    return (dispatch, getState) => {
        fetch(url)
            .then(response => response.json())
            .then(json => {
                console.log(json)
                dispatch(setNPword(json))
            });
    }
}
//initial state
const initialState={
   tags: localStorage.getItem("tags") ? localStorage.getItem("tags").split(',') : [],
};
//reducer

function reducer(state=initialState,action){
    switch(action.type){
        case SET_NEWS:
            return applySetNews(state, action);
        case SET_PWORD:
            return applySetPword(state, action);
        case SET_NPWORD:
            return applySetNPword(state, action);
        default:
            return state;
    }
}
//reducer functions 
function applySetNews(state,action){
    const {news} = action;
    return {
        ...state,
        news
    }
}
function applySetPword(state,action){
    const {pword} = action;
    return {
        ...state,
        pword
    }
}
function applySetNPword(state,action){
    const {npword} = action;
    return {
        ...state,
        npword
    }
}
//export 
const actionCreators ={
    getNews,
    getPword,
    getNPword
};
export {actionCreators};
//default reducer export

export default reducer;