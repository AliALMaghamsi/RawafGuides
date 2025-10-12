import { useState, useEffect } from "react";
import { DndContext, useDraggable, useDroppable } from "@dnd-kit/core";
import api from "../api/api";

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
  }, [selectedType]);

  // Fetch pilgrims (only after selecting room type)
  useEffect(() => {
    if (!selectedType) return;
    const fetchPilgrims = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/guide/hotels/rooms/${selectedType}/pilgrims`);
        setPilgrims(res.data);
      } catch {
        setError("Failed to load pilgrims.");
      } finally {
        setLoading(false);
      }
    };
    fetchPilgrims();
  }, [selectedType]);

  const handleDrop = async (pilgrimId, roomId) => {
    try {
      await api.put(`/api/guide/pilgrims/${pilgrimId}/`, { room_id: roomId });
      setPilgrims((prev) =>
        prev.map((p) =>
          p.id === pilgrimId ? { ...p, room_id: roomId } : p
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

      {/* Rooms and Unassigned Pilgrims */}
      {selectedType && (
        <div className="flex gap-4 w-2/4">
          <DndContext
            onDragEnd={(event) => {
              const pilgrimId = parseInt(event.active.id);
              const overId = event.over?.id;
              if (!overId) return;
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
                    .filter((p) => p.room_id === room.id)
                    .map((p) => (
                      <DraggablePilgrim key={p.id} pilgrim={p} />
                    ))}
                </DroppableRoom>
              ))}
            </div>

            {/* Unassigned Pilgrims */}
            <div className="w-1/2 bg-gray-50 rounded p-3 shadow-md">
              <h2 className="font-bold text-lg mb-3">Unassigned Pilgrims</h2>
              <DroppableRoom room={null}>
                {pilgrims
                  .filter((p) => !p.room_id)
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
