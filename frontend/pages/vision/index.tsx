// react component with typescript and bootstrap and axios and several buttons and input form fields for various routes like create ProductSet or create Product

import React from "react";

const Vision: React.FC = () => {

    return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="p-5 text-black text-center">
                <div>
                    Vision
                </div>
                <div>
                    <button className="btn btn-primary mx-2 my-2">Ping Backend</button>
                </div>

                <div>
                    <button className="btn btn-primary btn-constant-width mx-2 my-2">Information</button>
                </div>
            </div>
        </div>
    );

}

export default Vision;

