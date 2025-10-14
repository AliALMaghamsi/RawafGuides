import { useState, useEffect } from "react";
import { DndContext, useDraggable, useDroppable } from "@dnd-kit/core";
import api from "../api/api";

// Helper to get the correct room field for a pilgrim based on selected hotel
const getRoomFieldName = (pilgrim, hotelId) => {
      const hid = Number(hotelId);
     
      
      if (Number(pilgrim.h1_id) === hid) return "room_h1_id";
      if (Number(pilgrim.h2_id) === hid) return "room_h2_id";
      if (Number(pilgrim.h3_id) === hid) return "room_h3_id";
      return null;
};


// Get the room id for a pilgrim for the selected hotel
const getPilgrimRoomId = (pilgrim, hotelId) => {
  const field = getRoomFieldName(pilgrim, hotelId);
  if (!field) return null;
  return pilgrim[field];
};

const DraggablePilgrim = ({ pilgrim }) => {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id: pilgrim.id.toString(),
  });

  const style = {
    transform: transform
      ? `translate3d(${transform.x}px, ${transform.y}px, 0)`
      : undefined,
    cursor: "grab",
    border: "1px solid #ccc",
    padding: "6px",
    borderRadius: "6px",
    marginBottom: "4px",
    backgroundColor: "white",
  };

  return (
    <div ref={setNodeRef} {...listeners} {...attributes} style={style}>
      <p className="font-medium">{pilgrim.name}</p>
      <p className="text-sm text-gray-500">
        {pilgrim.passport_number} | {pilgrim.gender}
      </p>
    </div>
  );
};

const DroppableRoom = ({ room, children }) => {
  const { isOver, setNodeRef } = useDroppable({
    id: room ? room.id.toString() : "unassigned",
  });

  const style = {
    minHeight: "80px",
    padding: "8px",
    marginBottom: "8px",
    border: isOver ? "2px dashed green" : "1px solid #ccc",
    borderRadius: "6px",
    backgroundColor: room ? "#fefefe" : "#f9f9f9",
  };

  return (
    <div ref={setNodeRef} style={style}>
      {room && <p className="font-bold mb-1">Room {room.room_number}</p>}
      {children}
    </div>
  );
};

const GuideDashboard = () => {
  const [hotels, setHotels] = useState([]);
  const [selectedHotel, setSelectedHotel] = useState(null);
  const [roomTypes, setRoomTypes] = useState([]);
  const [selectedType, setSelectedType] = useState(null);
  const [rooms, setRooms] = useState([]);
  const [pilgrims, setPilgrims] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch hotels
  useEffect(() => {
    const fetchHotels = async () => {
      try {
        setLoading(true);
        const res = await api.get("/api/guide/hotels/");
        setHotels(res.data);
      } catch {
        setError("Failed to load hotels.");
      } finally {
        setLoading(false);
      }
    };
    fetchHotels();
  }, []);

  // Fetch room types
  useEffect(() => {
    if (!selectedHotel) return;
    const fetchRoomTypes = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/guide/hotels/${selectedHotel}/room-types/`);
        setRoomTypes(res.data);
        setSelectedType(null);
        setRooms([]);
        setPilgrims([]);
      } catch {
        setError("Failed to load room types.");
      } finally {
        setLoading(false);
      }
    };
    fetchRoomTypes();
  }, [selectedHotel]);

  // Fetch rooms
  useEffect(() => {
    if (!selectedHotel || !selectedType) return;
    const fetchRooms = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/guide/hotels/${selectedHotel}/rooms/${selectedType}`);
        setRooms(res.data);
      } catch {
        setError("Failed to load rooms.");
      } finally {
        setLoading(false);
      }
    };
    fetchRooms();
  }, [selectedHotel, selectedType]);

  // Fetch pilgrims
  useEffect(() => {
    if (!selectedHotel || !selectedType) return;
    const fetchPilgrims = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/guide/hotels/${selectedHotel}/rooms/${selectedType}/pilgrims`);
        setPilgrims(res.data);
      } catch {
        setError("Failed to load pilgrims.");
      } finally {
        setLoading(false);
      }
    };
    fetchPilgrims();
  }, [selectedHotel, selectedType]);

  const handleDrop = async (pilgrimId, roomId) => {
    const pilgrim = pilgrims.find((p) => p.id === pilgrimId);
    if (!pilgrim)return; 
    
    const fieldName = getRoomFieldName(pilgrim, selectedHotel);
    if (!fieldName)return;
    

    try {
      await api.put(`/api/guide/update/pilgrims/${selectedHotel}/${pilgrimId}/`, {
        room_id: roomId
      });

      // Update local state to reflect assignment
      setPilgrims((prev) =>
        prev.map((p) =>
          p.id === pilgrimId ? { ...p, [fieldName]: roomId } : p
        )
      );
    } catch {
      setError("Failed to assign/unassign pilgrim.");
    }
  };

  return (
    <div className="flex gap-4 p-6 overflow-x-auto">
      {/* Hotels */}
      <div className="w-1/4 bg-gray-50 rounded p-3 shadow-md">
        <h2 className="font-bold text-lg mb-3">Hotels</h2>
        {hotels.map((hotel) => (
          <div
            key={hotel.id}
            className={`p-2 rounded cursor-pointer ${
              selectedHotel === hotel.id ? "bg-blue-500 text-white" : "hover:bg-blue-100"
            }`}
            onClick={() => setSelectedHotel(hotel.id)}
          >
            {hotel.name}
          </div>
        ))}
      </div>

      {/* Room Types */}
      {roomTypes.length > 0 && (
        <div className="w-1/4 bg-gray-50 rounded p-3 shadow-md">
          <h2 className="font-bold text-lg mb-3">Room Types</h2>
          {roomTypes.map((type, i) => (
            <div
              key={i}
              className={`p-2 rounded cursor-pointer ${
                selectedType === type ? "bg-green-500 text-white" : "hover:bg-green-100"
              }`}
              onClick={() => setSelectedType(type)}
            >
              Type {type}
            </div>
          ))}
        </div>
      )}

      {/* Rooms & Unassigned */}
      {selectedType && (
        <div className="flex gap-4 w-2/4">
          <DndContext
            onDragEnd={(event) => {
            
            const pilgrimId = parseInt(event.active.id);
            const overId = event.over?.id;
            if (!overId) return console.log("No overId, drop ignored");
            const targetRoomId = overId === "unassigned" ? null : parseInt(overId);
            handleDrop(pilgrimId, targetRoomId);
          }}
          >
            {/* Rooms */}
            <div className="w-1/2 bg-gray-50 rounded p-3 shadow-md">
              <h2 className="font-bold text-lg mb-3">Rooms</h2>
              {rooms.map((room) => (
                <DroppableRoom key={room.id} room={room}>
                  {pilgrims
                    .filter((p) => getPilgrimRoomId(p, selectedHotel) === room.id)
                    .map((p) => (
                      <DraggablePilgrim key={p.id} pilgrim={p} />
                    ))}
                </DroppableRoom>
              ))}
            </div>

            {/* Unassigned */}
            <div className="w-1/2 bg-gray-50 rounded p-3 shadow-md">
              <h2 className="font-bold text-lg mb-3">Unassigned Pilgrims</h2>
              <DroppableRoom room={null}>
                {pilgrims
                  .filter((p) => !getPilgrimRoomId(p, selectedHotel))
                  .map((p) => (
                    <DraggablePilgrim key={p.id} pilgrim={p} />
                  ))}
              </DroppableRoom>
            </div>
          </DndContext>
        </div>
      )}
    </div>
  );
};

export default GuideDashboard;
