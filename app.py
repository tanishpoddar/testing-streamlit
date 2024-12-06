import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="SpeedScope", layout="wide")

# CSS styles from previous version

def speed_test_component():
    return """
    <script>
    async function getNetworkInfo() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            return {
                effectiveType: connection.effectiveType,
                downlink: connection.downlink,
                rtt: connection.rtt
            };
        }
        return null;
    }

    async function measureDownloadSpeed() {
        const startTime = performance.now();
        const fileUrl = 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png';
        
        try {
            const response = await fetch(fileUrl);
            const reader = response.body.getReader();
            let chunks = 0;
            
            while(true) {
                const {done, value} = await reader.read();
                if (done) break;
                chunks += value.length;
            }
            
            const endTime = performance.now();
            const durationInSeconds = (endTime - startTime) / 1000;
            const bitsLoaded = chunks * 8;
            const speedMbps = (bitsLoaded / (1024 * 1024)) / durationInSeconds;
            
            return speedMbps;
        } catch(error) {
            console.error('Error:', error);
            return 0;
        }
    }

    async function runSpeedTest() {
        const result = {download: 0, upload: 0, ping: 0};
        
        // Measure ping
        const pingStart = performance.now();
        await fetch('https://www.google.com/favicon.ico');
        result.ping = performance.now() - pingStart;

        // Get network info
        const networkInfo = await getNetworkInfo();
        if (networkInfo) {
            result.download = networkInfo.downlink;
            result.ping = networkInfo.rtt;
        } else {
            // Fallback to download speed test
            result.download = await measureDownloadSpeed();
        }

        // Simulated upload (typically 1/3 of download)
        result.upload = result.download / 3;

        // Send results back to Streamlit
        window.parent.Streamlit.setComponentValue(result);
    }

    runSpeedTest();
    </script>
    """

if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_results' not in st.session_state:
    st.session_state.current_results = {"download": 0, "upload": 0, "ping": 0}

st.markdown('<h1 class="main-title">🚀 SpeedScope</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your Internet Speed Analyzer</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Download Speed</p>
            <h2 class="metric-value">{st.session_state.current_results["download"]:.1f} Mbps</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Upload Speed</p>
            <h2 class="metric-value">{st.session_state.current_results["upload"]:.1f} Mbps</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Ping</p>
            <h2 class="metric-value">{st.session_state.current_results["ping"]:.0f} ms</h2>
        </div>
    """, unsafe_allow_html=True)

if st.button("Start Speed Test", type="primary"):
    with st.spinner("Testing your internet speed..."):
        components.html(speed_test_component(), height=0)
        
        # Add to history
        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **st.session_state.current_results
        })
        st.experimental_rerun()

if st.session_state.history:
    st.subheader("Speed History")
    recent_history = st.session_state.history[-10:]
    
    fig = go.Figure()
    timestamps = [entry["timestamp"].split()[1] for entry in recent_history]
    downloads = [entry["download"] for entry in recent_history]
    uploads = [entry["upload"] for entry in recent_history]
    
    fig.add_trace(go.Scatter(x=timestamps, y=downloads, name="Download", line=dict(color="#00b4d8", width=3)))
    fig.add_trace(go.Scatter(x=timestamps, y=uploads, name="Upload", line=dict(color="#90e0ef", width=3)))
    
    fig.update_layout(
        plot_bgcolor="#1a1f25",
        paper_bgcolor="#1a1f25",
        font_color="white",
        height=400,
        margin=dict(t=10),
        xaxis=dict(title="Time", gridcolor="#2a2f35"),
        yaxis=dict(title="Speed (Mbps)", gridcolor="#2a2f35")
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align: center;">Made with ❤️ by Tanish Poddar</p>', unsafe_allow_html=True)