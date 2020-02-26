import React, {useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { deepOrange, deepPurple } from '@material-ui/core/colors';
import {
    Paper,
    Grid,
    Typography,
    Avatar,
} from '@material-ui/core';

const useStyles = makeStyles(theme => ({
    paper: {
        padding: theme.spacing(2),
        color: theme.palette.text.secondary,
    },
    orange: {
        width: theme.spacing(8),
        height: theme.spacing(8),
        color: theme.palette.getContrastText(deepOrange[500]),
        backgroundColor: deepOrange[500],
    },
    purple: {
        width: theme.spacing(8),
        height: theme.spacing(8),
        color: theme.palette.getContrastText(deepPurple[500]),
        backgroundColor: deepPurple[500],
    },
}));

export default function Tweet(props) {
    const classes  = useStyles();

    return (
        <Grid item lg={8} xs={12} sm={10}>
            <Paper className={classes.paper}>
                <Grid container justify='center'>
                    <Grid item xs={1}>
                        <Avatar className={(classes.purple)}>OP</Avatar>
                    </Grid>
                    <Grid item xs={10}>
                        <Grid container justify='flex-start'>
                            <Grid item xs={12}>
                                <Typography variant="body2">Tue Feb 25 05:19:47 +0000 2020</Typography>
                            </Grid>
                            <Grid item xs={12}>
                                <Typography variant="body1" gutterBottom>
                                    RT @Dr_Engler: Learn Machine Learning with Python for Absolute Beginners https://t.co/MryKgVPpXM #machine-learning #python #numpy #data-sci…
                                </Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
        </Grid>
    );
}