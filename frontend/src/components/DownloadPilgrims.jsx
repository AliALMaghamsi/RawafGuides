import React from "react";
import api from "../api/api"; // your axios instance

const DownloadPilgrims = () => {
  const handleDownload = async () => {
    try {
      const response = await api.get("/api/admin/download/excelfile/", {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "pilgrims.xlsx");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  return (
    <div className="pt-10">
      <h1 className="text-xl font-bold mb-3">Download Pilgrims File</h1>
      <button
        onClick={handleDownload}
        className="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
      >
        Download
      </button>
    </div>
  );
};

export default DownloadPilgrims;
