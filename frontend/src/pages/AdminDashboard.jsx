import React from "react";
import UploadFile from "../components/uploadFile";
import DownloadPilgrims from "../components/downloadPilgrims";



const AdminDashboard = () => {
  return (
    <>
      <div className="flex  gap-x-52">
        <div className="pt-10 justify-start">
            <h1 className="pl-29 text-xl font-bold">Upload Guide file</h1>
            <UploadFile uploadUrl="/api/admin/upload/guides/" inputId="guides_input"/>
        </div>
        <div className="pt-10 place-self-center">
          
            <h1 className="pl-28 text-xl font-bold">Upload pilgrims file</h1>
            <UploadFile uploadUrl="/api/admin/upload/pilgrims/" inputId="pilgrims_input"/>
        
        </div>
        
      </div>
      <br />
      <div className="pl-10 pt-60">
        
        <DownloadPilgrims/>
        
      </div>
    </>
  )
}

export default AdminDashboard