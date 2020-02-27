import React, {useState, useEffect} from 'react';
import {
    Paper,
    Grid,
    Typography,
    Avatar,
    Fade,
} from '@material-ui/core';

import TweetStyles from 'styles/TweetStyles';

export default function Tweet(props) {
    // Set the props
    const tweetData = props.tweetData;

    // Handle fading effect of the tweet //
    const [fade, setFade] = useState(true);
    const [paperColor, setPaperColor] = useState('white');
    const [timeoutFadeObject, setTimeoutFadeObject] = useState(null);
    const [timeoutColorObject, setTimeoutColorObject] = useState(null);

    useEffect(() => {
        // If we have tweetData.fade, this means that this is the first tweet
        // on the list. Therefore, fade out and in again to show that this
        // tweet just arrived.
        if (tweetData.fade) {
            setFade(false);
            // Also change the color
            setPaperColor('newTweet');
            // Set fade back to true after 250 milliseconds
            const timeoutFade = setTimeout(() => {
                setFade(true);
            }, 250);
            setTimeoutFadeObject(timeoutFade);
            // Set color back to white after 250 milliseconds
            const timeoutColor = setTimeout(() => {
                setPaperColor('white');
            }, 2000);
            setTimeoutColorObject(timeoutColor);
        } else {
            // Make sure we clear/reset the timeouts in case we get alot of tweets at once
            // This prevents fading not happening as it should.
            clearTimeout(timeoutFadeObject);
            clearTimeout(timeoutColorObject);
        }
    }, [tweetData.id]);

    // Set the Styling
    const classes  = TweetStyles();

    // When the user clicks on the tweet's username
    const onClickUserName = () => {
        window.open(`https://twitter.com/${tweetData.user}`);
    };

    // When the user clicks on the tweet's text content
    const onClickTweet = () => {
        window.open(`https://twitter.com/${tweetData.user}/status/${tweetData.id}`);
    };

    const getUserAbbreviation = (userName) => {
        const names = userName.split('_');

        if (names.length == 1) {
            return names[0].substring(0,2).toUpperCase();
        }

        let abbreviation = '';

        names.slice(0,2).forEach(name => {
            abbreviation += name.charAt(0);
        });

        return abbreviation.toUpperCase();
    };

    // User avatar and name //
    const userAbbreviation = getUserAbbreviation(tweetData.user);

    const userName = <span className={classes.userName}
        onClick={onClickUserName} >
        {tweetData.user}
    </span>;

    // Tweet creation time and tweet header line //
    let createdAtDate = new Date(tweetData.created_at);
    createdAtDate = createdAtDate.toString().split('GMT')[0]; // HACK: remove the timezone
    const tweetHeader = `On ${createdAtDate} from
        ${tweetData.user_loc || 'an unknown location'}, `;

    const colorArray = [
        'orange', 'purple', 'pink', 'red', 'blue', 'cyan', 'blueGrey',
        'teal', 'green', 'lime', 'yellow', 'brown', 'grey'];
    const avatarColor = colorArray[tweetData.avatar_color_index];

    return (
        <Grid item lg={8} xs={12} sm={10}>
            <Fade in={fade}>
            <Paper className={`${classes.paper} ${classes[paperColor]}`}>
                <Grid container justify='center'>
                    <Grid item xs={1}>
                        <Avatar className={`${classes[avatarColor]} ${classes.avatar}`}
                            onClick={onClickUserName}>
                            {userAbbreviation}
                        </Avatar>
                    </Grid>
                    <Grid item xs={10}>
                        <Grid container justify='flex-start'>
                            <Grid item xs={12}>
                                <Typography variant="body2">{tweetHeader} {userName} wrote</Typography>
                            </Grid>
                            <Grid item xs={12}>
                                <Typography className={classes.tweetText}
                                    variant="body1" gutterBottom
                                    onClick={onClickTweet}>
                                    {tweetData.text}
                                </Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
            </Fade>
        </Grid>
    );
}
