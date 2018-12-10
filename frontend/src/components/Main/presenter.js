import React from "react";
import PropTypes from "prop-types";
import styles from "./styles.scss";
import Loading from "components/Loading";
import Music from "components/Music";
const Main = props => {
    if(props.loading){
        return <LoadingMain/>
    }
    else if(props.news){
        return <RenderTop100 {...props}/>
    }
}

const LoadingMain = props => (
    <div className={styles.main}>
        <Loading/>
    </div>
)

const RenderTop100 = props => (
    <div className={styles.main}>
        <div className={styles.whiteBox}>
         <div className={styles.date}>
            <span onClick={props.handleClick("True")} className={styles.btn}>&lt;</span>
           {props.time[props.index-1]} ~ {props.time[props.index]}
           <span onClick={props.handleClick("False")}className={styles.btn}>&gt; </span></div>
            <div className={styles.office}>{props.news.map(news=> <Box {...props}{...news}/>)}</div>
            <div className={styles.wordlist}>가장 많이 나온 단어</div>
            <div className={styles.list}>
                <div className={styles.notprogress}>
                    <div className={styles.word}>보수</div>
                    <div className={styles.leftbox}>{props.npword.map((npword,i)=> <Word i={i} {...props}{...npword}/>)}</div>
                </div>
                <div className={styles.progress}>
                    <div className={styles.word}>진보</div>
                    <div className={styles.leftbox}>{props.pword.map((pword,i)=> <Word i={i} {...props}{...pword}/>)}</div>
                </div>
            </div>
        </div>
    </div>
)
const Word = (props,context)=>{
    return(
        <div className={styles.columns}>
            <div className={styles.grade}>{props.i+1}.</div>
            <div className={styles.words}>{props.Word}</div>
            <div className={styles.count}>{props.Count}개</div>
        </div>
        //<div></div>
    )
}
const Box = (props, context) => {
    return(
        <div className={styles.box}>
            <div className={styles.Name}>
                {props.Percentage >= 50 ?
                    <div style={{color : '#00BFFF' }}>{props.Office_name}</div>
                    :
                     <div style={{color : '#FE642E' }}>{props.Office_name}</div>
                }  
            </div>
            <div className={styles.Percentage}>
                <div>진보율 : {props.Percentage}%</div>
            </div>
        </div>
    );

}
Main.propTypes = {
    handleClick : PropTypes.func.isRequired,
    url: PropTypes.string.isRequired,
}

export default Main;