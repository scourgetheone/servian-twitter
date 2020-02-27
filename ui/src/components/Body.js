import React, { useState, useEffect } from "react";
import {
    Snackbar,
    Grid,
    Typography,
    CircularProgress,
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';
import 'typeface-roboto';
import request from 'superagent';
import io from 'socket.io-client';
const env = process.env.NODE_ENV;

import Tweet from 'components/Tweet';
import MainStyles from 'styles/MainStyles';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

/**
 * The Body component renders the main page, including the welcoming header,
 * and the the list of tweets from the back-end.
 */
export default function Body() {
    /** Initialize React states and effects
     *
     */
    const [errorMessage, setErrorMessage] = useState('');
    // This socket object is used for setting up the websocket connection
    // and making sure that we only establish the connection up once.
    const [socket, setSocket] = useState(null);
    // Store the raw json data from the backend
    const [data, setData] = useState(null);
    // Save the list of tweets separately, so that we can add real-time tweets later
    const [tweets, setTweets] = useState([]);
    const [openErrorSnackbar, setOpenErrorSnackbar] = React.useState(false);

    const fetchData = () => {
        request
            .get('/load_previous_tweets')
            .then(res => {
                setData(res.body);
                setTweets(res.body.tweets);
            })
            .catch(err => {
                setErrorMessage(`${err.message}. Response code: ${err.response}`);
            });
    };

    /** NOTE: pass [data.length] in useEffect to tell React to stop applying
     * the effect if there hasn't been any new data. Nevertheless, there will
     * not be new data as we only fetch the initial data from the backend once.
     */
    useEffect(() => {
        fetchData();

        /** Socket.io event handlers
         *
         */
        let http = 'http://';
        if (env === 'production') {
            http = 'https://';
        }

        if (!socket) {
            const _socket = io(http + document.domain + ':' + location.port);
            setSocket(_socket);

            // Verify that the connection is working
            _socket.on('connect', function() {
                console.log('Websocket connected!');
            });

            // Handle the here_are_tweets event from the backend
            _socket.on('here_are_tweets', function(tweet) {
                console.log('tweet received', tweet);
                setTweets((tweets) => {
                    let newTweets = [].concat(tweets);
                    newTweets.unshift(tweet);
                    // Show a maximum of 100 tweets on the screen
                    newTweets = newTweets.slice(0,100);
                    return newTweets;
                });
            });
        }

    }, [data && data.length]);

    /** Display tweet information that was fetched from the back-end
     *
     */
    let tweetsDisplay = <Grid item xs={12}>
        <Grid container justify="center">
            <CircularProgress />
        </Grid>
    </Grid>;
    let streamKeyword;

    if (data && tweets) {
        tweetsDisplay = tweets.map((tweetData, i) => {
            if (i==0) {
                tweetData.fade = true;
            } else {
                tweetData.fade = false;
            }
            return <Tweet key={i} tweetData={tweetData}/>;
        });
        streamKeyword = data.stream_keyword;
    }

    /** Use the customized styling classes
     *
     */
    const classes = MainStyles();

    /** Handle the logic for the error message snackbar
     *
     */
    const handleCloseErrorSnackBar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpenErrorSnackbar(false);
    };

    return (
        <div className={classes.root}>
        <Grid container
            spacing={3}
            justify="center">
            <Grid item lg={7} xs={6}>
                <br />
                <br />
                <Typography className={classes.title} variant="h5">
                    Welcome to <span className={classes.servianFont}>Servian</span>'s real-time Twitter stream,
                    proudly serving you today all things <b>{streamKeyword}</b>
                </Typography>
            </Grid>
            {tweetsDisplay}
        </Grid>
        <Snackbar open={openErrorSnackbar} autoHideDuration={6000} onClose={handleCloseErrorSnackBar}>
            <Alert onClose={handleCloseErrorSnackBar} severity="error">
                {errorMessage}
            </Alert>
        </Snackbar>
    </div>
    );
}

