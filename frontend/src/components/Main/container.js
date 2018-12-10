import React, {Component} from "react";
import Main from "./presenter";
import PropTypes from "prop-types";

class Container extends Component{
    state = {
        loading:true,
        time: ['20181106','20181113', '20181120','20181127', '20181203'],
        index : 4
    };
    static propTypes = {
        getNews: PropTypes.func.isRequired,
        getPword: PropTypes.func.isRequired,
        getNPword: PropTypes.func.isRequired,
    };
    click = (boolleft) => event => {
        const {getNews} = this.props;
        const {getNPword} = this.props;
        const {getPword} = this.props;
        console.log(boolleft)
        console.log(this.state.index)
        if(boolleft == "True"){
            if(this.state.index>1){
                this.setState({
                    index : this.state.index -1
                })
                getNews(this.state.time[this.state.index-1]);
                getPword(this.state.time[this.state.index-1]);
                getNPword(this.state.time[this.state.index-1]);
            }
        }
        else{
            if(this.state.index<4){
                this.setState({
                    index : this.state.index + 1
                })
                getNews(this.state.time[this.state.index+1]);
                getPword(this.state.time[this.state.index+1]);
                getNPword(this.state.time[this.state.index+1]);
            }
        }
    }
    componentDidMount(){
        const {getNews} = this.props;
        const {getNPword} = this.props;
        const {getPword} = this.props;
        if(!this.props.news){
            if(!this.props.pword){
                if(!this.props.npword){
                    getNews(this.state.time[this.state.index]);
                    getPword(this.state.time[this.state.index]);
                    getNPword(this.state.time[this.state.index]);
                }
            }
        }
        else{
            if (this.props.news) {
                if (this.props.pword) {
                    if (this.props.npword) {
                        this.setState({
                            loading: false
                        });
                    }
                }
            }
        }
    };
    componentWillReceiveProps = nextProps => {
        const {getNews} = this.props;
        if(nextProps.news){
            if (nextProps.pword) {
                    if (nextProps.npword) {
                    this.setState({
                        loading: false
                    });
                }
            }
        }/*
        if(nextProps.news==this.props.news){
            getNews(this.state.time);
        }*/
    };
    render(){
        const {time,index} = this.state;
        const {news} = this.props;
        const {pword} = this.props;
        const {npword} = this.props;
        return <Main handleClick={this.click}{...this.state} npword={npword}  pword={pword} news={news}/>
    }
}

export default Container;