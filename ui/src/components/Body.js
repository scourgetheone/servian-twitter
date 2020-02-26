import React, { useState, useEffect } from "react";
import { makeStyles } from '@material-ui/core/styles';
import {
    Snackbar,
    Grid,
    Typography,
    CircularProgress,
} from '@material-ui/core';
import MuiAlert from '@material-ui/lab/Alert';
import 'typeface-roboto';
import request from 'superagent';

import Tweet from 'components/Tweet';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const useStyles = makeStyles(theme => ({
    root: {
      flexGrow: 1,
    },
    title: {
        textAlign: 'center',
    },
    servianFont: {
        color: 'orange',
        'font-weight': 'bold'
    },
}));

/**
 * The Body component renders the main page, including the welcoming header,
 * and the the list of tweets from the back-end.
 */
export default function Body() {
    // Initialize React states and effects //
    const [errorMessage, setErrorMessage] = useState('');
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

    /* NOTE: pass [data.length] in to tell React to stop applying the effect
    if there hasn't been any new data.
    */
    useEffect(() => {
        fetchData();
    }, [data && data.length]);

    // Display tweet information that was fetched from the back-end //
    let tweetsDisplay = <Grid item xs={12}>
        <Grid container justify="center">
            <CircularProgress />
        </Grid>
    </Grid>;
    let streamKeyword;

    if (data) {
        tweetsDisplay = tweets.map((tweetData, i) => <Tweet key={i} tweetData={tweetData}/>);
        streamKeyword = data.stream_keyword;
    }

    // Use the customized styling classes //
    const classes = useStyles();

    // Handle the logic for the error message snackbar //
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

