/*!

=========================================================
* Argon Dashboard React - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
//import ImageGallery from './ImageGallery';
import "../../assets/css/custom.css"

// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  Container,
  Row,
  Col,
  CardTitle,
  Button,
  Table,
  UncontrolledCollapse,
  ButtonDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem, Badge, Progress
} from "reactstrap";
// core components
import Header from "../../components/Headers/Header.js";
import Maps from "./Maps_Component.js";
import { Redirect } from "react-router-dom";

const PREFIX_URL = 'https://raw.githubusercontent.com/xiaolin/react-image-gallery/master/static/';
//const MEDIA_URL='/media/'

function fix_date(st) {
  let date = st.split('T');
  let year = date[0];
  let time = date[1].split('.')[0];
  return year + " " + time;
}

class AccidentDetails extends React.Component {
  constructor(props) {
    super(props);

    this.timer = null;

    this.toggle = this.toggle.bind(this);
    this.changeValue = this.changeValue.bind(this);

    this.state = {
      table_data : [],
      showIndex: false,
      showBullets: true,
      infinite: true,
      showThumbnails: true,
      showFullscreenButton: true,
      showGalleryFullscreenButton: true,
      showPlayButton: false,
      showGalleryPlayButton: false,
      showNav: true,
      isRTL: false,
      slideDuration: 5,
      slideInterval: 2000,
      slideOnThumbnailOver: false,
      thumbnailPosition: 'left',
      showVideo: {},
      video_total: 0,
      photos_total: 0,
      data: {
          id: '',
          location:
          {
            coords: { lat: '0', lng: '0' }
          },
          time: '',
          speed: '',
          address: '',
     },
      dropDownValue: 0,
      dropDownOpen: false,
      error:false,
    };
    this.numImg = 0
    this.images = [
      {
        thumbnail: ``,
        original: ``,
        source: '',
        renderItem: this._renderVideo.bind(this)
      },
      {
        original: ``,
        thumbnail: ``,
        imageSet: [
          {
            srcSet: `${PREFIX_URL}image_set_cropped.jpg`,
            media: '(max-width: 1280px)',
          },
          {
            srcSet: `${PREFIX_URL}image_set_default.jpg`,
            media: '(min-width: 1280px)',
          }
        ]
      },
      {
        original: `${PREFIX_URL}1.jpg`,
        thumbnail: `${PREFIX_URL}1t.jpg`,
        originalClass: 'featured-slide',
        thumbnailClass: 'featured-thumb',
      }
    ]
  }


  get_data = async (id) => {

    let response = await fetch(
      `/statistics/bus?id=${id}`);
    let result = await response.json();
    this.setState(prevState => (
      {
        data: {
          id: result['id'],
          location:
          {
            coords: { lat: result['latitude'], lng: result['longitude'] }
          },
          time: result['time'],
          speed: result['speed'],
          address: result['location']
     }
      }
    ));
    console.log(this.state.data)

    const response1 = await fetch(
              `/statistics/location_bus?id=${this.state.data.id}&time=ALL`
          );

          const result1 = await response1.json();
          console.log(result1)
          if(result1.length===0)
              this.setState(
             prevState => (
                 {
                     error: "No Buses to Show"
                 }
             )
         );
          else
              this.setState(
                  prevState => (
                      {
                          table_data: result1,
                          error: false
                      }
                  )
              );

  }

  componentDidMount() {
    let id = this.props.match.params['id']
    this.get_data(id)
    this.timer = setInterval(() => this.get_data(id), 10000)
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.slideInterval !== prevState.slideInterval ||
      this.state.slideDuration !== prevState.slideDuration) {
      // refresh setInterval
      this._imageGallery.pause();
      this._imageGallery.play();
    };
  }

  componentWillUnmount() {
    clearInterval(this.timer)
    this.timer = null
  }

  renderCars = (value, index) => {
    return (
      <tr key={index} >
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["time"]}
          </span>
        </th>
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["location"]}
          </span>
        </th>
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["latitude"]}
          </span>
        </th>
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["longitude"]}
          </span>
        </th>
        <th scope="row" style={{ textAlign: "center" }}>
          <span className="mr-2">{value["speed"]}</span>
          <div>
            <Progress
              max="100"
              value={value["speed"]}
              barClassName={this.getBarColor(value["speed"])}
            />
          </div>
        </th>
      </tr>
    )
  }

  _onImageClick(event) {
    console.debug('clicked on image', event.target, 'at index', this._imageGallery.getCurrentIndex());
  }

  _onImageLoad(event) {
    console.debug('loaded image', event.target.src);
  }

  _onSlide(index) {
    this._resetVideo();
    console.debug('slid to index', index);
  }

  _onPause(index) {
    console.debug('paused on index', index);
  }

  _onScreenChange(fullScreenElement) {
    console.debug('isFullScreen?', !!fullScreenElement);
  }

  _onPlay(index) {
    console.debug('playing from index', index);
  }

  _resetVideo() {
    this.setState({ showVideo: {} });

    if (this.state.showPlayButton) {
      this.setState({ showGalleryPlayButton: true });
    }

    if (this.state.showFullscreenButton) {
      this.setState({ showGalleryFullscreenButton: true });
    }
  }

  _toggleShowVideo(url) {
    this.state.showVideo[url] = !Boolean(this.state.showVideo[url]);
    this.setState({
      showVideo: this.state.showVideo
    });

    if (this.state.showVideo[url]) {
      if (this.state.showPlayButton) {
        this.setState({ showGalleryPlayButton: false });
      }

      if (this.state.showFullscreenButton) {
        this.setState({ showGalleryFullscreenButton: false });
      }
    }
  }

  _renderVideo(item) {
    return (
      <div>
        {
          this.state.showVideo[item.source] ?
            <div className='video-wrapper'>
              <a
                className='close-video'
                onClick={this._toggleShowVideo.bind(this, item.source)}
              >
              </a>
              <video autoPlay controls>
                  // width='100%'
                // height='100%'
                <source
                  src={item.source}
                  type="video/mp4">

                </source>
                  // frameBorder='0'
              // allowFullScreen
              </video>
            </div>
            :
            <a onClick={this._toggleShowVideo.bind(this, item.source)}>
              <div className='play-button' />
              <img className='image-gallery-image' src={item.original} />
              {
                item.description &&
                <span
                  className='image-gallery-description'
                  style={{ right: '0', left: 'initial', height: '100%' }}
                >
                  {item.description}
                </span>
              }
            </a>
        }
      </div>
    );
  }

  onGoBack = () => {
    return <Redirect to="/admin/Buses" />
  }

  /* Status dropdown functions */
  toggle() {
    this.setState({ dropDownOpen: !this.state.dropDownOpen });
  }

  changeValue(e) {
    this.updateDBToSelectedStatus(e.currentTarget.textContent)
    this.setState({ dropDownValue: e.currentTarget.textContent })

  }

  getBarColor(damage) {
    if (damage < 30) {
      return "h2 font-weight-bold mb-0 text-success"
    } else if (damage < 45) {
      return "h2 font-weight-bold mb-0 text-teal"
    } else if (damage < 75) {
      return "h2 font-weight-bold mb-0 text-orange"
    } else { return "h2 font-weight-bold mb-0 text-red" }
  }

  setStatusColor() {
    if (this.state.dropDownValue === "Accident resolved") {
      return (
        <Badge color="" className="badge-dot badge-lg">
          <i className="bg-lime" />
        </Badge>
      )
    }
    if (this.state.dropDownValue === "Emergency services are on their way") {
      return (
        <Badge color="" className="badge-dot badge-lg">
          <i className="bg-yellow" />
        </Badge>
      )
    }
    else {
      return (
        <Badge color="" className="badge-dot badge-lg">
          <i className="bg-red" />
        </Badge>
      )
    }
  }

  init_text_dropdown(id) {
    if (id === 2) {
      return ("Accident resolved")
    } else if (id === 1) {
      return ("Emergency services are on their way")
    } else { return ("Accident still not answered") }
  }

  updateDBToSelectedStatus(value) {
    if (value === "Accident resolved") {
      fetch(`/set_accident_status/${this.props.match.params['id']}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "status": 2
        })
      })
    }
    if (value === "Emergency services are on their way") {
      fetch(`/set_accident_status/${this.props.match.params['id']}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "status": 1
        })
      })
    }
    else {
      fetch(`/set_accident_status/${this.props.match.params['id']}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "status": 0
        })
      })
    }
  }
  handleClick = (e, id, value) => {
    e.preventDefault();
    let new_injured = this.state.accident_data.n_people_injured + value
    if (new_injured >= 0) {
      this.setState(() => (this.state.accident_data.n_people_injured = new_injured))
      this.set_injured(id, new_injured);
    }
  };

  set_injured(id, value) {
    fetch(`/set_accident_injured/${id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "injured": `${value}`
      })
    })
  }

  renderArray = (value,index) => {
    return(
      <tr key={index} >
        {/*<th scope="row" width="5%" style={{textAlign:"center"}}>*/}
        {/*  <span className="mb-0 text-sm">*/}
        {/*    {value["id"]}<br/>*/}
        {/*  </span>*/}
        {/*</th>*/}
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["time"]}
          </span>
        </th>
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["location"]}
          </span>
        </th>
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["latitude"]}
          </span>
        </th>
        <th scope="row" width="5%">
          <span className="mb-0 text-sm">
            {value["longitude"]}
          </span>
        </th>
       <th scope = "row" style={{textAlign:"center"}}>
           <span className="mr-2">{value["speed"]}</span>
           <div>
               <Progress
                  max="100"
                  value={value["speed"]}
                  barClassName={this.getBarColor(value["speed"])}
                />
            </div>
        </th>

      </tr>
    )
  }

  render() {
    return (
      <>
        <Header />
        <Container className=" mt--7" fluid>
          <Row>
            <Col className=" col">
              <Card className=" shadow">
                <CardHeader className=" bg-transparent">
                  <Row>
                    <Col>
                      <div className="d-flex">
                        <Button
                          className="icon icon-shape bg-info text-white rounded-circle shadow"
                          href="/#admin/Buses"
                          onClick={this.onGoBack()}
                        >
                          <i className="fas fa-angle-left" />
                        </Button>
                        <h2 className=" mt-2 ml-4 ">Bus {this.props.match.params['id']}</h2>
                      </div>
                    </Col>

                  </Row>
                </CardHeader>
                <CardBody>
                  <Row className="h-75 ">
                    <Maps
                      markers={[{
                        id: this.props.match.params['id'],
                        lat: this.state.data.location.coords.lat,
                        lng: this.state.data.location.coords.lng,

                      }]}
                      googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyD4aWR3SBGaa1oB0CuDf2vptnJfSMSguZU"
                      loadingElement={<div style={{ height: `100%` }} />}
                      center={this.state.data.location.coords}
                      zoom={17}

                      containerElement={
                        <div
                          className="map-canvas"
                          id="map-canvas"
                        />
                      }
                      mapElement={
                        <div style={{ height: `100%`, borderRadius: "inherit" }} />
                      }
                    />
                  </Row>
                  <CardHeader>
                    <h3>  </h3>
                  </CardHeader>
                  <Table bordered className="align-items-center table-light " hover >
                    <thead className="thead-light">
                      <tr >
                        <th scope="col " style={{ textAlign: "center" }}>
                          <div align="center" className="icon icon-shape bg-transparent text-dark rounded-circle">
                            <i className="fas fa-calendar-alt" />
                          </div>
                          <div >
                            <span className="ml-1">Date/Hour</span>
                          </div>
                        </th>
                        <th scope="col " style={{ textAlign: "center" }}>
                          <div align="center" className="icon icon-shape bg-transparent text-dark rounded-circle">
                            <i className="fas fa-map-marker" />
                          </div>
                          <div >
                            <span className="ml-1">Address</span>
                          </div>
                        </th>
                        <th scope="col" style={{ textAlign: "center" }}>
                          <div className="icon icon-shape bg-transparent text-dark rounded-circle" >
                            <i className="fas fa-map-marked-alt" />
                          </div>
                          <div >
                            <span className="ml-1">Latitude</span>
                          </div>
                        </th>
                        <th scope="col" style={{ textAlign: "center" }}>
                          <div className="icon icon-shape bg-transparent text-dark rounded-circle" >
                            <i className="fas fa-map-marked-alt" />
                          </div>
                          <div >
                            <span className="ml-1">Longitude</span>
                          </div>
                        </th>
                        <th scope="col" style={{ textAlign: "center" }}>
                          <div className="icon icon-shape bg-transparent text-dark rounded-circle" >
                            <i className="fas fa-tachometer-alt" />
                          </div>
                          <div >
                            <span className="ml-1">Velocity</span>
                          </div>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                    {this.state["table_data"].map(this.renderArray).reverse()}
                  </tbody>
                  </Table>

                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </>
    );
  }
}

export default AccidentDetails;
