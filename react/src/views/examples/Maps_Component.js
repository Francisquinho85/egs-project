import React from "react";
// react plugin used to create google maps
import {GoogleMap, Marker, withGoogleMap, withScriptjs} from "react-google-maps";
// core components


const MapWrapper = withScriptjs(
    withGoogleMap(props => 
    <GoogleMap
            defaultCenter= {props.defaultCenter}
            defaultZoom={props.zoom}
            defaultOptions={{
              // scrollwheel: false,
            }}
        >
        {props.markers.map((props,index) =>{

          return(
          <Marker position={{lat: props.lat, lng: props.lng}}
           key={index}
           id={index}
           // options={{icon:`/accident_icon/${props.status}`}}
              options={{icon:"/assets/img/icons/bus.png"}}
           onClick={(() => 
            { if(props.id)
                {window.location.href =`/#admin/accident_details/${props.id}`}
              }
              )}
             />
            )})}
        </GoogleMap>
    ));
  
  const MapWrapper_details = withScriptjs(
    withGoogleMap(props => <GoogleMap
            center= {props.center}
            defaultZoom={props.zoom}
            defaultOptions={{
              // scrollwheel: false,
            }}
        >
        {props.markers.map(props =>
          <Marker 
          position={{lat: props.lat, lng: props.lng}}
            options={{icon:"/assets/img/icons/bus.png"}}
           onClick={(() => 
            { if(props.id)
                {window.location.href =`/#admin/accident_details/${props.id}`}
              }
              )}
             />
        )}
        </GoogleMap>
    ));

class Maps extends React.Component {

  constructor(props){
    super(props);

    this.state = {
      lat: 41.148679887696275,
      lng: -8.637576907768661
    }
  }

  componentDidMount(){
    Promise.all([this.get_my_location()]).then((value) => {
      this.setState(
        {
          lat: 41.148679887696275, //value[0].coords.latitude,
          lng: -8.637576907768661//value[0].coords.longitude
        })})
  }

  get_my_location = () => {
    if (navigator.geolocation) {
      return new Promise(
        (resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject)
      )
    } else {
      return new Promise(
        resolve => resolve({})
      )
    }
  }

  render() 
  {
    if (this.props.center)
      return(
        <MapWrapper_details
        googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyDxoYS3cRSwGK_fT5KMzi_9PAUmZocg1A4"
        loadingElement={<div style={{ height: `100%` }} />}
        center = {this.props.center}
        zoom = {this.props.zoom}
        markers = {this.props.markers}
        containerElement={
            <div
                className="map-canvas"
                id="map-canvas"
            />
        }
        mapElement={this.props.mapElement}
    />
    )
    return (
    <MapWrapper
        googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyDxoYS3cRSwGK_fT5KMzi_9PAUmZocg1A4"
        loadingElement={<div style={{ height: `100%` }} />}
        defaultCenter = {this.state}
        zoom = {this.props.zoom}
        markers = {this.props.markers}
        containerElement={
            <div
                className="map-canvas"
                id="map-canvas"
            />
        }
        mapElement={this.props.mapElement}
    />

    );
  }
}

export default Maps;
