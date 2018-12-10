import { connect } from "react-redux";
import Container from "./container";
import {actionCreators as MusicActions} from "redux/modules/music";

const mapStateToProps = (state,ownprops) => {
    const {music : {news}} = state;
    const {music : {pword}} = state;
    const {music : {npword}} = state;
    return{
        news,
        pword,
        npword
    };
}
const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        getNews: (Time) => {
            dispatch(MusicActions.getNews(Time));
        },
        getPword: (Time) => {
            dispatch(MusicActions.getPword(Time));
        },
        getNPword: (Time) => {
            dispatch(MusicActions.getNPword(Time));
        },
    };
};
export default connect(mapStateToProps,mapDispatchToProps)(Container);